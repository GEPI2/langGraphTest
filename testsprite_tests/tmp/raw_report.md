
# TestSprite AI Testing Report(MCP)

---

## 1️⃣ Document Metadata
- **Project Name:** langGraphTest
- **Date:** 2025-12-05
- **Prepared by:** TestSprite AI Team

---

## 2️⃣ Requirement Validation Summary

#### Test TC001
- **Test Name:** test_graph_editor_node_drag_and_drop
- **Test Code:** [TC001_test_graph_editor_node_drag_and_drop.py](./TC001_test_graph_editor_node_drag_and_drop.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 77, in <module>
  File "<string>", line 34, in test_graph_editor_node_drag_and_drop
AssertionError: Failed to create node 1: {"detail":"Not Found"}

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/97107430-a56d-4e5d-992d-eaa6c427bb50/249e952a-e9c2-48c9-bf3a-b4b754574747
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC002
- **Test Name:** test_graph_execution_trigger
- **Test Code:** [TC002_test_graph_execution_trigger.py](./TC002_test_graph_execution_trigger.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 62, in <module>
  File "<string>", line 31, in test_graph_execution_trigger
AssertionError: Graph creation failed: {"detail":[{"type":"literal_error","loc":["body","nodes",0,"type"],"msg":"Input should be 'LLMNode', 'CodeNode', 'RAGNode', 'HumanNode', 'StartNode' or 'EndNode'","input":"START","ctx":{"expected":"'LLMNode', 'CodeNode', 'RAGNode', 'HumanNode', 'StartNode' or 'EndNode'"}}]}

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/97107430-a56d-4e5d-992d-eaa6c427bb50/d2d29da4-59be-490c-bb86-904e9d70cbf0
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC003
- **Test Name:** test_rag_dashboard_document_upload
- **Test Code:** [TC003_test_rag_dashboard_document_upload.py](./TC003_test_rag_dashboard_document_upload.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/97107430-a56d-4e5d-992d-eaa6c427bb50/25b784be-9a14-4740-b1ea-79f12a7da55f
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC004
- **Test Name:** test_rag_dashboard_retrieval_testing
- **Test Code:** [TC004_test_rag_dashboard_retrieval_testing.py](./TC004_test_rag_dashboard_retrieval_testing.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 46, in <module>
  File "<string>", line 20, in test_rag_dashboard_retrieval_testing
AssertionError: Upload response missing success status

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/97107430-a56d-4e5d-992d-eaa6c427bb50/3c879f85-d32e-45af-b17b-deaa7b568003
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC005
- **Test Name:** test_mcp_dashboard_server_registration
- **Test Code:** [TC005_test_mcp_dashboard_server_registration.py](./TC005_test_mcp_dashboard_server_registration.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 62, in <module>
  File "<string>", line 25, in test_mcp_dashboard_server_registration
AssertionError: Expected 201 Created but got 422

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/97107430-a56d-4e5d-992d-eaa6c427bb50/a7302919-19c9-4146-be49-da762e46ff06
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC006
- **Test Name:** test_mcp_dashboard_tool_listing
- **Test Code:** [TC006_test_mcp_dashboard_tool_listing.py](./TC006_test_mcp_dashboard_tool_listing.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 53, in <module>
  File "<string>", line 24, in test_mcp_dashboard_tool_listing
AssertionError: Failed to register MCP server: {"detail":"Failed to connect to MCP server Test MCP Server: [Errno 2] No such file or directory"}

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/97107430-a56d-4e5d-992d-eaa6c427bb50/b35010e3-837f-424a-88fb-2895626fce27
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC007
- **Test Name:** test_finetuning_dashboard_job_creation
- **Test Code:** [TC007_test_finetuning_dashboard_job_creation.py](./TC007_test_finetuning_dashboard_job_creation.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 70, in <module>
  File "<string>", line 33, in test_finetuning_dashboard_job_creation
AssertionError: Expected 201 Created, got 422

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/97107430-a56d-4e5d-992d-eaa6c427bb50/8ae03be0-f6e7-47ff-a832-289bae63597d
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC008
- **Test Name:** test_finetuning_dashboard_job_monitoring
- **Test Code:** [TC008_test_finetuning_dashboard_job_monitoring.py](./TC008_test_finetuning_dashboard_job_monitoring.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 72, in <module>
  File "<string>", line 30, in test_finetuning_dashboard_job_monitoring
AssertionError: Expected status code 201, got 404

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/97107430-a56d-4e5d-992d-eaa6c427bb50/12e187b4-d5f4-4456-8a27-cb880d8321ec
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC009
- **Test Name:** test_backend_api_graph_saving_and_loading
- **Test Code:** [TC009_test_backend_api_graph_saving_and_loading.py](./TC009_test_backend_api_graph_saving_and_loading.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 102, in <module>
  File "<string>", line 48, in test_backend_api_graph_saving_and_loading
AssertionError: Failed to save graph config: {"detail":"Unknown node type: StartNode"}

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/97107430-a56d-4e5d-992d-eaa6c427bb50/3f017a01-7f15-46d3-9419-094b77104d8f
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC010
- **Test Name:** test_backend_api_error_handling_for_invalid_inputs
- **Test Code:** [TC010_test_backend_api_error_handling_for_invalid_inputs.py](./TC010_test_backend_api_error_handling_for_invalid_inputs.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 104, in <module>
  File "<string>", line 88, in test_backend_api_error_handling_for_invalid_inputs
AssertionError: Expected status 422 but got 404 for POST http://localhost:8001/graph/save with payload {'invalidField': 123}. Response body: {"detail":"Not Found"}

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/97107430-a56d-4e5d-992d-eaa6c427bb50/b04822eb-ea06-4992-b013-c95613333bb6
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---


## 3️⃣ Coverage & Matching Metrics

- **10.00** of tests passed

| Requirement        | Total Tests | ✅ Passed | ❌ Failed  |
|--------------------|-------------|-----------|------------|
| ...                | ...         | ...       | ...        |
---


## 4️⃣ Key Gaps / Risks
{AI_GNERATED_KET_GAPS_AND_RISKS}
---