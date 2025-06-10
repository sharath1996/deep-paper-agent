from agent.agents.search_and_infer import SearchAndInferAgent, SearchAndInferInput
import json

def test_search_and_infer():
    """
    Test the SearchAndInfer agent's search and inference capabilities.
    This test will simulate a search for the capital of France and verify the output.
    """
    # Create an instance of the SearchAndInfer agent
    local_obj_searchAndInfer = SearchAndInferAgent()

    # Define the input parameters for the search
    local_obj_search_input = SearchAndInferInput(str_task="Create a getting started guide for IPCM drivers in arm used for embedded systems for STM32 devices")

    # Perform the search and inference
    local_obj_inferenceOutput = local_obj_searchAndInfer.run(local_obj_search_input)

    with open(".results/test_search_and_infer_results.json", "w") as local_obj_file:
        json.dump(local_obj_inferenceOutput.model_dump(), local_obj_file, indent=4)