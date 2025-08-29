# AI Orchestra Build Workflow

## Step 1: Initiate Core Framework with GitHub Copilot
1. Open VSCode with GitHub Copilot enabled
2. Create new Python files in a project directory:
   - investigation_core.py
   - timeline_generator.py
   - contradiction_detector.py
   - email_document_linker.py
3. For each file, prompt Copilot with the specific requirements from prompts/copilot/core_framework.md
4. Save completed files to responses/copilot/

## Step 2: Develop Medical Analyzer with ChatGPT
1. Go to chat.openai.com and start a new conversation
2. Copy and paste the ENTIRE contents of prompts/chatgpt/medical_analyzer.md
3. Copy the generated code and save to responses/chatgpt/medical_analyzer.py
4. Review the code for any obvious issues or missing functionality

## Step 3: Create Contradiction Detector with Claude
1. Go to claude.ai and start a new conversation
2. Copy and paste the ENTIRE contents of prompts/claude/contradiction_detector.md
3. Copy the generated code and save to responses/claude/contradiction_detector.py
4. Review the code for any obvious issues or missing functionality

## Step 4: Generate Test Suite with Claude
1. Go to claude.ai and start a new conversation
2. Copy and paste the ENTIRE contents of prompts/claude/test_suite.md
3. Copy the generated code and save to responses/claude/tests/
4. Review the tests for any obvious issues or missing test cases

## Step 5: Create Documentation with Bard/Gemini
1. Go to bard.google.com and start a new conversation
2. Copy and paste the ENTIRE contents of prompts/bard/documentation.md
3. Copy the generated documentation and save to responses/bard/
4. Review the documentation for any obvious issues or missing information

## Step 6: Integration
1. Run the integration script: ./integrate_components.sh
2. Review the integrated code in the integrated/ directory
3. Fix any integration issues or conflicts

## Step 7: Iterative Improvement
1. For any component that needs improvement, create a specific improvement prompt
2. Return to the appropriate AI with the code and improvement request
3. Update the corresponding file in responses/
4. Re-run integration and testing

## Step 8: Final Review
1. Have each AI review the fully integrated system
2. Implement any final improvements
3. Complete final testing and documentation
