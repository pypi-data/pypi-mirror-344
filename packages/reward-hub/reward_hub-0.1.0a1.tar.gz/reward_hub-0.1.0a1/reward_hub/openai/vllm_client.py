import concurrent.futures
import time
import requests

class vllmClient:
    def __init__(self, model_name, port):
        self.model_name = model_name
        self.port = port
    
    def make_vllm_request(  # noqa
        self,
        batch_prompts,
        max_new_tokens=4096,
        temperature=0.8,
        top_k=50,
        top_p=0.85,
        stop_sequences=None,
        num_workers=40,
        logprobs = 0,
        echo = False,
        use_beam_search=False,
    ):
        """Sampling parameters for text generation.
        Only batch_prompts is required to run it.
        logprobs = 0, do not return log probs in the result;
        echo = False, do not return log probs for inputs 
        """
        port = self.port
        model_name = self.model_name
        endpoint=f"http://localhost:{port}/v1/completions"


        headers = {"Content-type": "application/json"}

        def post_request(body):
            tries = 10
            for j in range(tries):  # 10 retries
                try:
                    response = requests.post(endpoint, json=body, headers=headers)
                    jres = response.json()
                    assert "choices" in jres, "invalid outputs, resubmit request {jres}"
                except Exception as e:
                    if j < tries - 1:
                        print("Timeout connection to vLLM, waiting 5 secs before retry")
                        print(e)
                        print("Prompts Lengths:", len(body["prompt"].split()))
                        time.sleep(5)
                        continue
                    else:
                        raise e
                break

            response_json = response.json()  # Assuming the response is in JSON format
            response_json["input_prompt"] = body["prompt"]  # Add 'input_prompt' to response JSON
            return response_json

        def post_requests(bodies):
            return [post_request(body) for body in bodies]

        results = []

        if not num_workers:
            num_workers = len(batch_prompts)
        else:
            num_workers = min(num_workers, len(batch_prompts))

        def create_request_instance(prompt_str, stop_sequences):
            request_body = {
                "model": model_name,
                "prompt": prompt_str,
                "max_tokens": max_new_tokens,
                "temperature": temperature,
                "stop": stop_sequences,
                "top_p": top_p,
                "top_k": top_k,
                "use_beam_search": use_beam_search,
                "echo": echo,
                "logprobs": logprobs
            }
            return request_body

        # Chunk prompt data into evenly distributed pieces to for each worker
        def serialize_worker(batch_prompts, num_workers):
            """
            Returns chunked batch_prompts, where len(chunked_prompts) == num_workers,
            and ensures that when chunked_prompts are flattened, they equal batch_prompts.
            """
            assert num_workers <= len(
                batch_prompts
            ), "Error, number of workers must be less than or equal to batch_size"

            # Calculate the size of each chunk
            chunk_size = len(batch_prompts) // num_workers
            extra = len(batch_prompts) % num_workers

            worker_chunks = []
            start = 0
            for i in range(num_workers):
                # Adjust the end index to include an extra item for the first few chunks if needed
                end = start + chunk_size + (1 if i < extra else 0)

                # Ensures that the correct stop sequence is passed to each prompt_instance
                chunk_ls = [create_request_instance(batch_prompts[j], stop_sequences) for j in range(start, end)]
                worker_chunks.append(chunk_ls)
                start = end

            return worker_chunks

        worker_chunks = serialize_worker(batch_prompts, num_workers)
        # test that the worker chunks can be decoded into the original sequence
        assert [
            x["prompt"] for x in sum(worker_chunks, [])
        ] == batch_prompts, "The flattened chunked prompts do not match the original batch prompts"

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            # Submit all the request batches to be processed by post_requests function
            api_results = list(executor.map(post_requests, worker_chunks))
            for chunk_idx, chunk_results in enumerate(api_results):
                for item_idx, data in enumerate(chunk_results):
                    assert (
                        data["input_prompt"] == worker_chunks[chunk_idx][item_idx]["prompt"]
                    ), "output order is incorrect compared with submitted input order"
                    
                    results.append(
                        dict(
                            input_text=worker_chunks[chunk_idx][item_idx]["prompt"],
                            generated_text=data["choices"][0]["text"].strip(),
                            stop_reason="",
                            stop_sequence=worker_chunks[chunk_idx][item_idx]["stop"],
                            logprobs=data['choices'][0]['logprobs'] if "logprobs" in data['choices'][0] else None
                        )
                    )

        assert [
            x["input_text"] for x in results
        ] == batch_prompts, "The resulting prompt is different from original batch prompt"

        return results


    def vllm_request_logprobs(  # noqa
        self,
        batch_prompts,
        num_workers=40,
    ):
        raw_request_outputs = self.make_vllm_request(  # noqa
            batch_prompts=batch_prompts,
            temperature = 0,
            max_new_tokens=0,
            num_workers=num_workers,
            logprobs = 1,
            echo = "true"
        )
        tokens, token_logprobs = self.post_process_logprobs(raw_request_outputs)
        return tokens, token_logprobs 

    def post_process_logprobs(self, raw_outputs):
        for output in raw_outputs:
            assert "logprobs" in output, "log prob is not available in the outputs"
        
        return [x["logprobs"]["tokens"] for x in raw_outputs], [x["logprobs"]["token_logprobs"] for x in raw_outputs]

