import os
import time
from agent_g.agent import GeminiAgent

# Set your Gemini API key
os.environ["GEMINI_API_KEY"] = "your-api-key-here"

def main():
    print("Initializing Gemini Agent...")
    agent = GeminiAgent()
    
    while True:
        try:
            # Get user instruction
            instruction = input("\nEnter instruction (or 'exit' to quit): ")
            
            if instruction.lower() == 'exit':
                break
                
            # Process and execute
            print("Processing...")
            start_time = time.time()
            
            result = agent.run(instruction)
            
            execution_time = time.time() - start_time
            print(f"\nCompleted in {execution_time:.2f} seconds")
            print(f"Success: {result['success']}")
            print(f"\nExplanation:")
            print(result['explanation'])
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()