# AI Modules Documentation

This document provides a comprehensive overview of all AI, ML, LLM, and chatbot-related modules in the ai-script-inventory repository.

## Overview

The repository contains **6299** AI-related modules organized across multiple categories. These modules provide extensive functionality for working with various AI services, frameworks, and tools.

## Import Conventions

**IMPORTANT**: All imports have been standardized to use Python's standard library modules:

- ✅ Use `from types import ModuleType` (NOT `from types_mod import`)
- ✅ Use `from typing import List, Dict` (NOT `from typing_mod import`)
- ✅ Use `from enum import Enum` (NOT `from enum_mod_custom import`)
- ✅ Use `from pathlib import Path` (NOT `from pathlib_mod_custom import`)

## Module Categories


### Other AI Tools (3921 modules)

#### `ai_tools/arrow_parser_wrapper.py`

**Description**: Wrapper for the pyarrow engine for read_csv()...

**Key Classes**: ArrowParserWrapper

**AI Keywords**: text, ai, inference

---

#### `ai_tools/brain_numpy_core_function_base.py`

**Description**: Astroid hooks for numpy.core.function_base module....

**AI Keywords**: ai, ml, inference

---

#### `ai_tools/from_dataframe.py`

**Description**: Build a ``pd.DataFrame`` from any DataFrame supporting the interchange protocol.

    .. note::

       For new development, we highly recommend using the Arrow C Data Interface
       alongside the A...

**AI Keywords**: ai

---

#### `ai_tools/_helper.py`

**Description**: Discrete Fourier Transforms - _helper.py...

**AI Keywords**: ai

---

#### `ai_tools/logging_callback_manager.py`

**Description**: A centralized class that allows easy add / remove callbacks for litellm.

    Goals of this class:
    - Prevent adding duplicate callbacks / success_callback / failure_callback
    - Keep a reasonabl...

**Key Classes**: LoggingCallbackManager

**AI Keywords**: ai, ml, llm

---

#### `ai_tools/probability_fixt.py`

**AI Keywords**: ai

---

#### `ai_tools/test_remote.py`

**Description**: Cloning shouldn't fail...

**AI Keywords**: ai, ml

---

#### `ai_tools/conversation_item_retrieve_event.py`

**Description**: The ID of the item to retrieve....

**Key Classes**: ConversationItemRetrieveEvent

**AI Keywords**: ai, model

---

#### `ai_tools/test_build_meta.py`

**Description**: PEP 517 Build Backend...

**Key Classes**: BuildBackendBase, BuildBackend, BuildBackendCaller, TestBuildMetaBackend, TestBuildMetaLegacyBackend

**AI Keywords**: text, ai, ml

---

#### `ai_tools/test_mincost.py`

**Description**: Combinatorial Optimization: Algorithms and Complexity,
        Papadimitriou Steiglitz at page 140 has an example, 7.1, but that
        admits multiple solutions, so I alter it a bit. From ticket #43...

**Key Classes**: TestMinCostFlow

**AI Keywords**: ai

---

#### `ai_tools/test_split_partition.py`

**AI Keywords**: ai

---

#### `ai_tools/sftp_si.py`

**Description**: An interface to override for SFTP server support....

**Key Classes**: SFTPServerInterface

**AI Keywords**: text, ai, ml, chat, together

---

#### `ai_tools/test_graph6.py`

**Description**: See gh-7557...

**Key Classes**: TestGraph6Utils, TestFromGraph6Bytes, TestReadGraph6, TestWriteGraph6, TestToGraph6Bytes

**AI Keywords**: ai

---

#### `ai_tools/brain_collections.py`

**Description**: class defaultdict(dict):
        default_factory = None
        def __missing__(self, key): pass
        def __getitem__(self, key): return default_factory...

**AI Keywords**: text, ai, ml, inference

---

#### `ai_tools/test_terminal.py`

**Description**: Basic tests for the Superhuman AI Terminal components....

**AI Keywords**: text, ai

---

#### `ai_tools/test_dominating.py`

**Description**: In complete graphs each node is a dominating set.
    Thus the dominating set has to be of cardinality 1....

**AI Keywords**: ai

---

#### `ai_tools/counter.py`

**Description**: Language Model Counter
----------------------...

**Key Classes**: NgramCounter

**AI Keywords**: text, ai, model

---

#### `ai_tools/create_numpy_pickle.py`

**Description**: This script is used to generate test data for joblib/test/test_numpy_pickle.py...

**AI Keywords**: ai

---

#### `ai_tools/aiohttp_transport.py`

**Description**: LiteLLM wrapper around AiohttpTransport to handle %-encodings in URLs
    and event loop lifecycle issues in CI/CD environments

    Credit to: https://github.com/karpetrosyan/httpx-aiohttp for this i...

**Key Classes**: AiohttpResponseStream, AiohttpTransport, LiteLLMAiohttpTransport

**AI Keywords**: text, ai, llm

---

#### `ai_tools/test_contraction.py`

**Description**: Unit tests for the :mod:`networkx.algorithms.minors.contraction` module....

**AI Keywords**: ai, model

---

*... and 3901 more modules in this category*


### Multimodal AI (468 modules)

#### `ai_tools/backend_qt.py`

**Description**: A context manager that allows terminating a plot by sending a SIGINT....

**Key Classes**: TimerQT, FigureCanvasQT, MainWindow, FigureManagerQT, NavigationToolbar2QT

**AI Keywords**: image, text, ai, ml

---

#### `ai_tools/response_input_content_param.py`

**AI Keywords**: image, text, ai

---

#### `ai_tools/conversation_item_input_audio_transcription_failed_event.py`

**Description**: Error code, if any....

**Key Classes**: Error, ConversationItemInputAudioTranscriptionFailedEvent

**AI Keywords**: ai, audio, model

---

#### `ai_tools/na.py`

**Description**: No application cache available (most likely as we don't have write permissions)....

**Key Classes**: AppDataDisabled, ContentStoreNA

**AI Keywords**: image, text, ai

---

#### `ai_tools/versionpredicate.py`

**Description**: Module for parsing and testing package version predicate strings....

**Key Classes**: VersionPredicate

**AI Keywords**: vision, ai

---

#### `ai_tools/test_vocab_api.py`

**Description**: Test Vocab.__contains__ works with int keys....

**AI Keywords**: speech, text, nlp, ai, spacy

---

#### `ai_tools/input_audio_buffer_append_event.py`

**Description**: Base64-encoded audio bytes.

    This must be in the format specified by the `input_audio_format` field in the
    session configuration....

**Key Classes**: InputAudioBufferAppendEvent

**AI Keywords**: ai, audio, model

---

#### `ai_tools/texmanager.py`

**Description**: Support for embedded TeX expressions in Matplotlib.

Requirements:

* LaTeX.
* \*Agg backends: dvipng>=1.6.
* PS backend: PSfrag, dvips, and Ghostscript>=9.0.
* PDF and SVG backends: if LuaTeX is pres...

**Key Classes**: TexManager

**AI Keywords**: image, text, ai

---

#### `ai_tools/katz.py`

**Description**: Katz centrality....

**AI Keywords**: vision, ai

---

#### `ai_tools/socks.py`

**Description**: This module contains provisional support for SOCKS proxies from within
urllib3. This module supports SOCKS4, SOCKS4A (an extension of SOCKS4), and
SOCKS5. To enable its functionality, either install P...

**Key Classes**: SOCKSConnection, SOCKSHTTPSConnection, SOCKSHTTPConnectionPool, SOCKSHTTPSConnectionPool, SOCKSProxyManager

**AI Keywords**: text, vision, ai, ml

---

#### `ai_tools/test_datetime64.py`

**Key Classes**: TestDatetime64ArrayLikeComparisons, TestDatetime64SeriesComparison, TestDatetimeIndexComparisons, TestDatetime64Arithmetic, TestDatetime64DateOffsetArithmetic

**AI Keywords**: vision, ai

---

#### `ai_tools/cu2qu.py`

**Description**: Return the dot product of two vectors.

    Args:
        v1 (complex): First vector.
        v2 (complex): Second vector.

    Returns:
        double: Dot product....

**AI Keywords**: vision, ai, google

---

#### `ai_tools/node_classification.py`

**Description**: This module provides the functions for node classification problem.

The functions in this module are not imported
into the top level `networkx` namespace.
You can access these functions by importing
...

**AI Keywords**: neural, vision, ai, ml, classification

---

#### `ai_tools/image_file_delta_block.py`

**Description**: The index of the content part in the message....

**Key Classes**: ImageFileDeltaBlock

**AI Keywords**: image, ai, model

---

#### `ai_tools/WmfImagePlugin.py`

**Description**: Install application-specific WMF image handler.

    :param handler: Handler object....

**Key Classes**: WmfStubImageFile

**AI Keywords**: image, ai, ml

---

#### `ai_tools/audio_to_audio.py`

**Description**: Inputs for Audio to Audio inference...

**Key Classes**: AudioToAudioInput, AudioToAudioOutputElement

**AI Keywords**: huggingface, ai, audio, inference

---

#### `ai_tools/categorical.py`

**Description**: Helper for membership check for ``key`` in ``cat``.

    This is a helper method for :method:`__contains__`
    and :class:`CategoricalIndex.__contains__`.

    Returns True if ``key`` is in ``cat.cat...

**Key Classes**: Categorical, CategoricalAccessor

**AI Keywords**: text, vision, ai, ml, inference, together

---

#### `ai_tools/easy_input_message.py`

**Description**: Text, image, or audio input to the model, used to generate a response. Can also
    contain previous assistant responses....

**Key Classes**: EasyInputMessage

**AI Keywords**: image, text, ai, audio, model

---

#### `ai_tools/test_linux.py`

**Description**: Linux specific tests....

**Key Classes**: TestSystemVirtualMemoryAgainstFree, TestSystemVirtualMemoryAgainstVmstat, TestSystemVirtualMemoryMocks, TestSystemSwapMemory, TestSystemCPUTimes

**AI Keywords**: text, vision, ai, ml

---

#### `ai_tools/input_audio_buffer_commit_event_param.py`

**Description**: The event type, must be `input_audio_buffer.commit`....

**Key Classes**: InputAudioBufferCommitEventParam

**AI Keywords**: ai, audio

---

*... and 448 more modules in this category*


### LLM Providers (463 modules)

#### `ai_tools/response_custom_tool_call_output.py`

**Description**: The call ID, used to map this custom tool call output to a custom tool call....

**Key Classes**: ResponseCustomToolCallOutput

**AI Keywords**: openai, ai, model

---

#### `ai_tools/handler.py`

**Description**: Handler for transforming /chat/completions api requests to litellm.responses requests...

**Key Classes**: ResponsesToCompletionBridgeHandlerInputKwargs, ResponsesToCompletionBridgeHandler

**AI Keywords**: openai, completion, ai, ml, chat, llm, model

---

#### `ai_tools/_scilab_builtins.py`

**Description**: pygments.lexers._scilab_builtins
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Builtin list for the ScilabLexer.

    :copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
    :license: BSD, ...

**AI Keywords**: image, completion, text, generation, eval, ai, ml, bert, llm, aws

---

#### `ai_tools/codeagent.py`

**Description**: A Coding Agent (CodeAgent)

A re-interpretation for CAI of the original CodeAct concept
from the paper "Executable Code Actions Elicit Better LLM Agents"
at https://arxiv.org/pdf/2402.01030.

Briefly,...

**Key Classes**: CodeAgentException, CodeGenerationError, CodeParsingError, CodeExecutionError, CodeExecutionTimeoutError

**AI Keywords**: openai, completion, text, generation, detection, ai, chat, llm, prompt, model

---

#### `ai_tools/litellm.py`

**AI Keywords**: openai, completion, text, claude, gpt, ai, chat, llm, model

---

#### `ai_tools/base_utils.py`

**Description**: Utility functions for base LLM classes....

**Key Classes**: BaseLLMModelInfo

**AI Keywords**: openai, completion, claude, eval, ai, chat, llm, anthropic, bedrock, model

---

#### `ai_tools/strict_schema.py`

**Description**: Mutates the given JSON schema to ensure it conforms to the `strict` standard
    that the OpenAI API expects....

**AI Keywords**: openai, ai, model

---

#### `ai_tools/prompt_caching_deployment_check.py`

**Description**: Check if prompt caching is valid for a given deployment

Route to previously cached model id, if valid...

**Key Classes**: PromptCachingDeploymentCheck

**AI Keywords**: openai, completion, eval, ai, ml, llm, prompt, model

---

#### `ai_tools/amazon_nova_canvas_transformation.py`

**Description**: Reference: https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/model-catalog/serverless/amazon.nova-canvas-v1:0...

**Key Classes**: AmazonNovaCanvasConfig

**AI Keywords**: image, openai, text, generation, amazon, ai, llm, aws, bedrock, model

---

#### `ai_tools/openai_tts.py`

**Description**: A text-to-speech model for OpenAI....

**Key Classes**: OpenAITTSModel

**AI Keywords**: speech, openai, text, ai, audio, model

---

#### `ai_tools/code_interpreter_output_image.py`

**Description**: The [file](https://platform.openai.com/docs/api-reference/files) ID of the
    image....

**Key Classes**: Image, CodeInterpreterOutputImage

**AI Keywords**: image, openai, ai, model

---

#### `ai_tools/anthropic_claude3_transformation.py`

**Description**: Call Claude model family in the /v1/messages API spec...

**Key Classes**: AmazonAnthropicClaude3MessagesConfig, AmazonAnthropicClaudeMessagesStreamDecoder

**AI Keywords**: completion, claude, amazon, ai, ml, chat, llm, aws, anthropic, bedrock

---

#### `ai_tools/proxy_server.py`

**Description**: Asynchronously checks if the request is disconnected at regular intervals.
    If the request is disconnected
    - cancel the litellm.router task
    - raises an HTTPException with status code 499 an...

**Key Classes**: UserAPIKeyCacheTTLEnum, StreamingCallbackError, ProxyConfig, ProxyStartupEvent

**AI Keywords**: speech, image, openai, gemini, completion, text, azure, generation, llama, huggingface

---

#### `ai_tools/test_trace_processor.py`

**Description**: Create a minimal agent span for testing processors....

**AI Keywords**: openai, text, ai

---

#### `ai_tools/required_action_function_tool_call.py`

**Description**: The arguments that the model expects you to pass to the function....

**Key Classes**: Function, RequiredActionFunctionToolCall

**AI Keywords**: openai, ai, model

---

#### `ai_tools/get_llm_provider_logic.py`

**Description**: if user sets model = "cohere/command-r" -> use custom_llm_provider = "cohere_chat"

    Args:
        model:
        custom_llm_provider:

    Returns:
        model, custom_llm_provider...

**AI Keywords**: image, openai, gemini, completion, text, claude, azure, nlp, generation, llama

---

#### `ai_tools/chat_completion_assistant_message_param.py`

**Description**: Unique identifier for a previous audio response from the model....

**Key Classes**: Audio, FunctionCall, ChatCompletionAssistantMessageParam

**AI Keywords**: openai, completion, text, ai, audio, chat, model

---

#### `ai_tools/_emoji_codes.py`

**AI Keywords**: speech, gemini, llama, vision, safety, ai, bert, bard, together, comet

---

#### `ai_tools/image_file_delta.py`

**Description**: Specifies the detail level of the image if specified by the user.

    `low` uses fewer tokens, you can opt in to high resolution using `high`....

**Key Classes**: ImageFileDelta

**AI Keywords**: image, openai, vision, ai, model

---

#### `ai_tools/basic_usage.py`

**Description**: A common tactic is to break down a task into a series of smaller steps. 
Each task can be performed by an agent, and the output of one agent is used as input to the next
try stream and normal...

**AI Keywords**: openai, completion, ai, chat, model

---

*... and 443 more modules in this category*


### AI Safety & Guardrails (127 modules)

#### `ai_tools/ExifTags.py`

**Description**: This module provides constants and clear-text names for various
well-known EXIF tags....

**Key Classes**: Base, GPS, Interop, IFD, LightSource

**AI Keywords**: image, text, eval, safety, ai, ml, classification, model

---

#### `ai_tools/file_finder.py`

**Description**: Determines whether a given path should be excluded based on the provided exclusion set.

    Args:
        excludes (Set[Path]): Set of paths to exclude.
        to_analyze (Path): The path to analyze...

**Key Classes**: FileFinder

**AI Keywords**: safety, model

---

#### `ai_tools/test_custom_dtypes.py`

**Description**: The addition method is special for the scaled float, because it
        includes the "cast" between different factors, thus cast-safety
        is influenced by the implementation....

**Key Classes**: TestSFloat

**AI Keywords**: safety, ai

---

#### `ai_tools/global_usage_tracker.py`

**Description**: Global usage tracker that persists usage data to $HOME/.cai/usage.json...

**Key Classes**: GlobalUsageTracker

**AI Keywords**: safety, ai, model

---

#### `ai_tools/project.py`

**Key Classes**: ProjectModel

**AI Keywords**: safety, ai, model

---

#### `ai_tools/tzinfo.py`

**Description**: Factory function for unpickling pytz tzinfo instances.

    This is shared for both StaticTzInfo and DstTzInfo instances, because
    database changes could cause a zones implementation to switch betw...

**Key Classes**: BaseTzInfo, StaticTzInfo, DstTzInfo

**AI Keywords**: safety, ai

---

#### `ai_tools/test_validators.py`

**Description**: One can create a validator class whose metaschema uses a different
        dialect than itself....

**Key Classes**: TestCreateAndExtend, TestValidationErrorMessages, TestValidationErrorDetails, MetaSchemaTestsMixin, ValidatorTestMixin

**AI Keywords**: text, eval, safety, ai, train

---

#### `ai_tools/zero_five.py`

**Description**: Schema for CVSSv2 data.

    Attributes:
        base_score (fields_.Int): Base score of the CVSSv2.
        impact_score (fields_.Int): Impact score of the CVSSv2.
        vector_string (fields_.Str)...

**Key Classes**: CVSSv2, CVSSv3, VulnerabilitySchemaV05

**AI Keywords**: safety, ai

---

#### `ai_tools/telemetry.py`

**Description**: Telemetry object generated per Safety report; this model holds data related to the
    client application running Safety CLI....

**Key Classes**: TelemetryModel

**AI Keywords**: safety, ai, model

---

#### `ai_tools/astype.py`

**Description**: Functions for implementing 'astype' methods according to pandas conventions,
particularly ones that differ from numpy....

**AI Keywords**: safety, ai

---

#### `ai_tools/init_scan.py`

**Description**: Types of scan results that can be yielded by the init_scan function...

**Key Classes**: ScanResultType, BaseScanResult, InitScanResult, ProgressScanResult, CompleteScanResult

**AI Keywords**: text, safety, ai, ml, model

---

#### `ai_tools/report_protocol.py`

**Key Classes**: ReportConvertible

**AI Keywords**: safety, ai, model

---

#### `ai_tools/guardrail_initializers.py`

**AI Keywords**: text, guardrail, detection, ai, llm, aws, moderation, bedrock

---

#### `ai_tools/test_callback.py`

**Description**: \
        a = t(fun,[fun_extra_args])

        Wrapper for ``t``.

        Parameters
        ----------
        fun : call-back function

        Other Parameters
        ----------------
        fun...

**Key Classes**: TestF77Callback, TestF77CallbackPythonTLS, TestF90Callback, TestGH18335, TestGH25211

**AI Keywords**: text, safety, ai

---

#### `ai_tools/organize_ai_scripts.py`

**Description**: Organize and audit root directory of repository by file type.
Moves files to type-based folders, ensures required templates exist,
and logs all actions. Designed for CI automation and safe local use.
...

**AI Keywords**: text, detection, safety, ai, ml

---

#### `ai_tools/moderation_model.py`

**AI Keywords**: text, ai, moderation, model

---

#### `ai_tools/emission.py`

**Description**: Emit an event and immediately flush the event bus without closing it.

    Args:
        event_bus: The event bus to emit on
        event: The event to emit...

**AI Keywords**: text, detection, safety, ai, model, together

---

#### `ai_tools/output_utils.py`

**Description**: Build the content for the announcements section.

    Args:
        announcements (List[Dict[str, Any]]): List of announcements.
        columns (int, optional): Number of columns for formatting. Defa...

**AI Keywords**: text, safety, ai, ml, prompt, model

---

#### `ai_tools/logging_mod.py`

**Description**: Raised if BrokenPipeError occurs for the stdout stream while logging....

**Key Classes**: BrokenStdoutLoggingError, IndentingFormatter, IndentedRenderable, PipConsole, RichPipStreamHandler

**AI Keywords**: text, safety, ai

---

#### `ai_tools/spend_tracking_utils.py`

**Description**: Generate a stable hash from a response object.

    Args:
        response_obj: The response object to hash (can be dict, list, etc.)

    Returns:
        A hex string representation of the MD5 hash...

**AI Keywords**: completion, text, guardrail, ai, llm, prompt, model

---

*... and 107 more modules in this category*


### AI Framework Integrations (5 modules)

#### `ai_tools/argilla.py`

**Description**: Send logs to Argilla for annotation...

**Key Classes**: ArgillaLogger

**AI Keywords**: completion, text, langsmith, ai, ml, chat, llm, model

---

#### `ai_tools/team_callback_endpoints.py`

**Description**: Endpoints to control callbacks per team

Use this when each team should control its own callbacks...

**AI Keywords**: langsmith, ai, llm, model

---

#### `ai_tools/test_registry.py`

**AI Keywords**: mlflow, ai, ml, spacy, wandb, clearml, pytorch

---

#### `ai_tools/langsmith.py`

**Description**: for /batch langsmith requires id, trace_id and dotted_order passed as params...

**Key Classes**: LangsmithLogger

**AI Keywords**: completion, text, langsmith, langchain, ai, llm, model

---

#### `ai_tools/insecure_hashlib.py`

**AI Keywords**: mlflow, huggingface, transformer, ai, ml

---


### AI Evaluation & Testing (577 modules)

#### `ai_tools/test_serialize_config.py`

**Description**: [paths]
train = null
dev = null

[corpora]

[corpora.train]
@readers = "spacy.Corpus.v1"
path = ${paths.train}

[corpora.dev]
@readers = "spacy.Corpus.v1"
path = ${paths.dev}

[training]

[training.ba...

**AI Keywords**: nlp, eval, ai, ml, spacy, model, train

---

#### `ai_tools/evaluate.py`

**Description**: Evaluate a trained pipeline. Expects a loadable spaCy pipeline and evaluation
    data in the binary .spacy format. The --gold-preproc option sets up the
    evaluation examples with gold-standard sen...

**AI Keywords**: text, nlp, eval, ai, ml, spacy, model, train

---

#### `ai_tools/_g_v_a_r.py`

**Description**: > # big endian
	version:			H
	reserved:			H
	axisCount:			H
	sharedTupleCount:		H
	offsetToSharedTuples:		I...

**Key Classes**: table__g_v_a_r

**AI Keywords**: text, eval, ai, ml

---

#### `ai_tools/md_in_html.py`

**Description**: Parse Markdown syntax within raw HTML.
Based on the implementation in [PHP Markdown Extra](http://michelf.com/projects/php-markdown/extra/).

See the [documentation](https://Python-Markdown.github.io/...

**Key Classes**: HTMLExtractorExtra, HtmlBlockPreprocessor, MarkdownInHtmlProcessor, MarkdownInHTMLPostprocessor, MarkdownInHtmlExtension

**AI Keywords**: text, eval, ai, ml

---

#### `ai_tools/capi_maps.py`

**Description**: Copyright 1999 -- 2011 Pearu Peterson all rights reserved.
Copyright 2011 -- present NumPy Developers.
Permission to use, modify, and distribute this software is given under the
terms of the NumPy Lic...

**AI Keywords**: eval, ai, ml

---

#### `ai_tools/build_env.py`

**Description**: Build Environment used for isolation during sdist building...

**Key Classes**: _Prefix, BuildEnvironmentInstaller, SubprocessBuildEnvironmentInstaller, BuildEnvironment, NoOpBuildEnvironment

**AI Keywords**: text, eval, ai

---

#### `ai_tools/rolling.py`

**Description**: Provide a generic structure to support window functions,
similar to how we have a Groupby object....

**Key Classes**: BaseWindow, BaseWindowGroupby, Window, RollingAndExpandingMixin, Rolling

**AI Keywords**: text, vision, eval, ai, ml

---

#### `ai_tools/modulefinder.py`

**Description**: Low-level infrastructure to find modules.

This builds on fscache.py; find_sources.py builds on top of this....

**Key Classes**: SearchPaths, ModuleNotFoundReason, BuildSource, BuildSourceSet, FindModuleCache

**AI Keywords**: text, eval, ai, ml, together

---

#### `ai_tools/nist_score.py`

**Description**: NIST score implementation....

**AI Keywords**: eval, ai

---

#### `ai_tools/_asyncio.py`

**Description**: Shutdown and close event loop....

**Key Classes**: CancelScope, TaskState, _AsyncioTaskStatus, TaskGroup, WorkerThread

**AI Keywords**: text, eval, ai, aws

---

#### `ai_tools/truncate.py`

**Description**: Utilities for truncating assertion output.

Current default behaviour is to truncate assertion explanations at
terminal lines, unless running with an assertions verbosity level of at least 2 or runnin...

**AI Keywords**: eval, ai

---

#### `ai_tools/_k_e_r_n.py`

**Description**: Kerning table

    The ``kern`` table contains values that contextually adjust the inter-glyph
    spacing for the glyphs in a ``glyf`` table.

    Note that similar contextual spacing adjustments can...

**Key Classes**: table__k_e_r_n, KernTable_format_0, KernTable_format_unkown

**AI Keywords**: text, eval, ai, ml

---

#### `ai_tools/_legacy_keywords.py`

**Description**: Ignore siblings of ``$ref`` if it is present.

    Otherwise, return all keywords.

    Suitable for use with `create`'s ``applicable_validators`` argument....

**AI Keywords**: text, eval, ai

---

#### `ai_tools/eval_delete_response.py`

**Key Classes**: EvalDeleteResponse

**AI Keywords**: eval, ai, model

---

#### `ai_tools/L_T_S_H_.py`

**Description**: Linear Threshold table

    The ``LTSH`` table contains per-glyph settings indicating the ppem sizes
    at which the advance width metric should be scaled linearly, despite the
    effects of any Tru...

**Key Classes**: table_L_T_S_H_

**AI Keywords**: text, eval, ai, ml

---

#### `ai_tools/eval_api_error.py`

**Description**: The error code....

**Key Classes**: EvalAPIError

**AI Keywords**: eval, ai, model

---

#### `ai_tools/k8s_attributes.py`

**Description**: The name of the cluster....

**Key Classes**: K8sContainerStatusReasonValues, K8sContainerStatusStateValues, K8sNamespacePhaseValues, K8sNodeConditionStatusValues, K8sNodeConditionTypeValues

**AI Keywords**: image, eval, ai, ml

---

#### `ai_tools/_add_newdocs.py`

**Description**: This is only meant to add docs to objects defined in C-extension modules.
The purpose is to allow easier editing of the docstrings without
requiring a re-compile.

NOTE: Many of the methods of ndarray...

**AI Keywords**: text, eval, ai, ml, together

---

#### `ai_tools/rcsetup.py`

**Description**: The rcsetup module contains the validation code for customization using
Matplotlib's rc settings.

Each rc setting is assigned a function used to validate any attempted changes
to that setting.  The v...

**Key Classes**: __getattr__, ValidateInStrings, _DunderChecker, _ignorecase

**AI Keywords**: image, text, eval, ai, ml, together, train

---

#### `ai_tools/chunkparser_app.py`

**Description**: A graphical tool for exploring the regular expression based chunk
parser ``nltk.chunk.RegexpChunkParser``....

**Key Classes**: RegexpChunkApp

**AI Keywords**: speech, text, eval, ai, train

---

*... and 557 more modules in this category*


### Training & Fine-tuning (379 modules)

#### `ai_tools/package.py`

**Description**: Generate an installable Python package for a pipeline. Includes binary data,
    meta and required installation files. A new directory will be created in the
    specified output directory, and the da...

**AI Keywords**: text, nlp, transformer, ai, ml, spacy, prompt, model, together, train

---

#### `ai_tools/hole.py`

**Description**: An implementation of the Hole Semantics model, following Blackburn and Bos,
Representation and Inference for Natural Language (CSLI, 2005).

The semantic representations are built by the grammar hole....

**Key Classes**: Constants, HoleSemantics, Constraint

**AI Keywords**: text, ai, model, inference, together, train

---

#### `ai_tools/hard_swish.py`

**AI Keywords**: ai, model, train

---

#### `ai_tools/test_link_prediction.py`

**Key Classes**: TestResourceAllocationIndex, TestJaccardCoefficient, TestAdamicAdarIndex, TestCommonNeighborCentrality, TestPreferentialAttachment

**AI Keywords**: ai, train

---

#### `ai_tools/swish.py`

**AI Keywords**: ai, model, train

---

#### `ai_tools/test_image.py`

**Description**: Test the interpolation of the alpha channel on RGBA images...

**Key Classes**: QuantityND

**AI Keywords**: image, text, ai, ml, together, train

---

#### `ai_tools/carbon.py`

**Description**: pygments.lexers.carbon
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexers for the Carbon programming language.

    :copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENS...

**Key Classes**: CarbonLexer

**AI Keywords**: text, ai, train

---

#### `ai_tools/test_textcat.py`

**Description**: [model]
@architectures = "spacy-legacy.HashEmbedCNN.v1"
pretrained_vectors = null
width = 96
depth = 4
embed_size = 2000
window_size = 1
maxout_pieces = 3
subword_features = true...

**AI Keywords**: text, nlp, ai, spacy, model, train

---

#### `ai_tools/erroranalysis.py`

**Description**: Returns a list of human-readable strings indicating the errors in the
    given tagging of the corpus.

    :param train_sents: The correct tagging of the corpus
    :type train_sents: list(tuple)
   ...

**AI Keywords**: text, ai, train

---

#### `ai_tools/scikitlearn.py`

**Description**: scikit-learn (https://scikit-learn.org) is a machine learning library for
Python. It supports many classification algorithms, including SVMs,
Naive Bayes, logistic regression (MaxEnt) and decision tre...

**Key Classes**: SklearnClassifier

**AI Keywords**: text, nlp, sklearn, transformer, ai, classification, model, train

---

#### `ai_tools/annotated_handlers.py`

**Description**: Type annotations to use with `__get_pydantic_core_schema__` and `__get_pydantic_json_schema__`....

**Key Classes**: GetJsonSchemaHandler, GetCoreSchemaHandler

**AI Keywords**: text, generation, ai, model, train

---

#### `ai_tools/util.py`

**Description**: Parse a marker string and return a dictionary containing a marker expression.

    The dictionary will contain keys "op", "lhs" and "rhs" for non-terminals in
    the expression grammar, or strings. A...

**Key Classes**: cached_property, FileOperator, ExportEntry, Cache, EventMixin

**AI Keywords**: text, ai, ml, prompt, together, train

---

#### `ai_tools/schema.py`

**Description**: Process a list of models and generate a single JSON Schema with all of them defined in the ``definitions``
    top-level JSON key, including their sub-models.

    :param models: a list of models to i...

**Key Classes**: SkipField

**AI Keywords**: ai, model, train

---

#### `ai_tools/array_getitem.py`

**Description**: Index into input arrays, and return the subarrays.

    index:
        A valid numpy-style index. Multi-dimensional indexing can be performed
        by passing in a tuple, and slicing can be performe...

**AI Keywords**: ai, model, train

---

#### `ai_tools/_tensorboard_logger.py`

**Description**: Contains a logger to push training logs to the Hub, using Tensorboard....

**Key Classes**: HFSummaryWriter

**AI Keywords**: text, huggingface, vision, ai, ml, model, pytorch, train

---

#### `ai_tools/structuralholes.py`

**Description**: Functions for computing measures of structural holes....

**AI Keywords**: vertex, ai, train

---

#### `ai_tools/elpi.py`

**Description**: pygments.lexers.elpi
    ~~~~~~~~~~~~~~~~~~~~

    Lexer for the `Elpi <http://github.com/LPCIC/elpi>`_ programming language.

    :copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
  ...

**Key Classes**: ElpiLexer

**AI Keywords**: text, ai, train

---

#### `ai_tools/tuplify.py`

**Description**: Send a separate copy of the input to each child layer, and join the
    outputs of the children into a tuple on the way out.

    Typically used to provide both modified data and the original input to...

**AI Keywords**: ai, model, train

---

#### `ai_tools/test_corpus.py`

**Description**: This is a doc. It contains two sentences.
This is another doc.

A third doc....

**AI Keywords**: text, nlp, ai, spacy, train

---

#### `ai_tools/supervised_hyperparameters_param.py`

**Description**: Number of examples in each batch.

    A larger batch size means that model parameters are updated less frequently, but
    with lower variance....

**Key Classes**: SupervisedHyperparametersParam

**AI Keywords**: ai, model, train

---

*... and 359 more modules in this category*


### Embeddings & Vector Search (74 modules)

#### `ai_tools/create_embedding_response.py`

**Description**: The number of tokens used by the prompt....

**Key Classes**: Usage, CreateEmbeddingResponse

**AI Keywords**: ai, embedding, prompt, model

---

#### `ai_tools/guardrails_ai.py`

**Description**: Runs on response from LLM API call

        It can be used to reject a response...

**Key Classes**: GuardrailsAIResponse, InferenceData, GuardrailsAIResponsePreCall, GuardrailsAI

**AI Keywords**: image, completion, text, generation, guardrail, ai, embedding, audio, llm, moderation

---

#### `ai_tools/backend_pdf.py`

**Description**: A PDF Matplotlib backend.

Author: Jouni K Seppänen <jks@iki.fi> and others....

**Key Classes**: Reference, Name, Verbatim, Op, Stream

**AI Keywords**: image, text, generation, vision, vertex, ai, embedding

---

#### `ai_tools/presidio.py`

**Description**: Construct the payload for the Presidio analyze request

        API Ref: https://microsoft.github.io/presidio/api-docs/api-docs.html#tag/Analyzer/paths/~1analyze/post...

**Key Classes**: _OPTIONAL_PresidioPIIMasking

**AI Keywords**: image, completion, text, guardrail, safety, ai, ml, embedding, chat, llm

---

#### `ai_tools/model_armor.py`

**Description**: Google Cloud Model Armor Guardrail integration for LiteLLM.

    Supports:
    - Pre-call sanitization (sanitizeUserPrompt)
    - Post-call sanitization (sanitizeModelResponse)...

**Key Classes**: ModelArmorGuardrail

**AI Keywords**: image, completion, text, generation, vertex, guardrail, ai, embedding, audio, llm

---

#### `ai_tools/dynamic_rate_limiter.py`

**Description**: Thin wrapper on DualCache for this file.

    Track number of active projects calling a model....

**Key Classes**: DynamicRateLimiterCache, _PROXY_DynamicRateLimitHandler

**AI Keywords**: image, completion, text, generation, ai, ml, embedding, audio, llm, moderation

---

#### `ai_tools/qdrant_semantic_cache.py`

**Description**: Qdrant Semantic Cache implementation

Has 4 methods:
    - set_cache
    - get_cache
    - async_set_cache
    - async_get_cache...

**Key Classes**: QdrantSemanticCache

**AI Keywords**: text, eval, ai, embedding, llm, prompt, model

---

#### `ai_tools/sambanova.py`

**Key Classes**: SambanovaConversationalTask, SambanovaFeatureExtractionTask

**AI Keywords**: huggingface, ai, embedding, model, inference

---

#### `ai_tools/features.py`

**Description**: Leaflet GeoJson and miscellaneous features....

**Key Classes**: RegularPolygonMarker, Vega, VegaLite, GeoJson, GeoJsonStyleMapper

**AI Keywords**: image, text, ai, ml, embedding, aws

---

#### `ai_tools/dispatch_interface.py`

**Key Classes**: LoopbackGraph, LoopbackDiGraph, LoopbackMultiGraph, LoopbackMultiDiGraph, LoopbackPlanarEmbedding

**AI Keywords**: generation, ai, embedding

---

#### `ai_tools/fontBuilder.py`

**Description**: This module is *experimental*, meaning it still may evolve and change.

The `FontBuilder` class is a convenient helper to construct working TTF or
OTF fonts from scratch.

Note that the various setup ...

**Key Classes**: FontBuilder

**AI Keywords**: text, vision, eval, ai, embedding

---

#### `ai_tools/parallel_request_limiter.py`

**Description**: Raise an HTTPException with a 429 status code and a retry-after header...

**Key Classes**: CacheObject, _PROXY_MaxParallelRequestsHandler

**AI Keywords**: completion, ai, ml, embedding, chat, llm, model

---

#### `ai_tools/openmeter.py`

**Description**: Expects
        OPENMETER_API_ENDPOINT,
        OPENMETER_API_KEY,

        in the environment...

**Key Classes**: OpenMeterLogger

**AI Keywords**: completion, text, ai, ml, embedding, llm, prompt, model

---

#### `ai_tools/parametricattention.py`

**Description**: Weight inputs by similarity to a learned vector...

**AI Keywords**: ai, ml, embedding, model, train

---

#### `ai_tools/caching_handler.py`

**Description**: This contains LLMCachingHandler 

This exposes two methods:
    - async_get_cache
    - async_set_cache

This file is a wrapper around caching.py

This class is used to handle caching logic specific f...

**Key Classes**: CachingHandlerResponse, LLMCachingHandler

**AI Keywords**: completion, text, ai, ml, embedding, audio, chat, llm, prompt, model

---

#### `ai_tools/redact_messages.py`

**Description**: Performs the actual redaction on the logging object and result....

**AI Keywords**: text, ai, ml, embedding, llm, prompt, model

---

#### `ai_tools/route_llm_request.py`

**Description**: Get the team id from the data's metadata or litellm_metadata params....

**Key Classes**: ProxyModelNotFoundError

**AI Keywords**: speech, image, completion, text, generation, ai, embedding, audio, chat, llm

---

#### `ai_tools/nebius.py`

**Key Classes**: NebiusTextGenerationTask, NebiusConversationalTask, NebiusTextToImageTask, NebiusFeatureExtractionTask

**AI Keywords**: image, text, generation, huggingface, ai, embedding, prompt, model, inference

---

#### `ai_tools/panw_prisma_airs.py`

**Description**: PANW Prisma AIRS Built-in Guardrail for LiteLLM...

**Key Classes**: PanwPrismaAirsHandler

**AI Keywords**: image, completion, text, generation, guardrail, detection, ai, embedding, audio, llm

---

#### `ai_tools/hashembed.py`

**Description**: An embedding layer that uses the “hashing trick” to map keys to distinct values.
    The hashing trick involves hashing each key four times with distinct seeds,
    to produce four likely differing va...

**AI Keywords**: text, ai, embedding, model, train

---

*... and 54 more modules in this category*


### Prompt Management (163 modules)

#### `ai_tools/vi.py`

**Description**: Return struct for functions wrapped in ``text_object``.
    Both `start` and `end` are relative to the current cursor position....

**Key Classes**: TextObjectType, TextObject

**AI Keywords**: completion, text, ai, ml, prompt

---

#### `ai_tools/tag_management.py`

**Key Classes**: TagBase, TagConfig, TagNewRequest, TagUpdateRequest, TagDeleteRequest

**AI Keywords**: completion, ai, llm, prompt, model

---

#### `ai_tools/murphy.py`

**Description**: pygments.styles.murphy
    ~~~~~~~~~~~~~~~~~~~~~~

    Murphy's style from CodeRay.

    :copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details....

**Key Classes**: MurphyStyle

**AI Keywords**: ai, prompt

---

#### `ai_tools/named_commands.py`

**Description**: Key bindings which are also known by GNU Readline by the given names.

See: http://www.delorie.com/gnu/docs/readline/rlman_13.html...

**AI Keywords**: completion, text, ai, ml, prompt

---

#### `ai_tools/hexdump.py`

**Description**: pygments.lexers.hexdump
    ~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for hexadecimal dumps.

    :copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for detail...

**Key Classes**: HexdumpLexer

**AI Keywords**: ai, prompt

---

#### `ai_tools/recraft.py`

**Description**: TypedDict for Recraft image edit request parameters.
    
    Based on Recraft API docs: https://www.recraft.ai/docs#image-to-image...

**Key Classes**: RecraftImageGenerationRequestParams, RecraftImageEditRequestParams

**AI Keywords**: image, text, generation, ai, prompt, model

---

#### `ai_tools/parallel_request_limiter_v3.py`

**Description**: This is a rate limiter implementation based on a similar one by Envoy proxy. 

This is currently in development and not yet ready for production....

**Key Classes**: RateLimitDescriptorRateLimitObject, RateLimitDescriptor, RateLimitStatus, RateLimitResponse, RateLimitResponseWithDescriptors

**AI Keywords**: completion, ai, ml, llm, prompt, model

---

#### `ai_tools/image_to_video.py`

**Description**: The size in pixel of the output video frames....

**Key Classes**: ImageToVideoTargetSize, ImageToVideoParameters, ImageToVideoInput, ImageToVideoOutput

**AI Keywords**: image, text, generation, huggingface, ai, prompt, model, inference

---

#### `ai_tools/replay.py`

**Description**: Tool to convert JSONL files to a replay format that simulates the CLI output.
This allows reviewing conversations in a more readable format.

Usage:
    JSONL_FILE_PATH="path/to/file.jsonl" REPLAY_DEL...

**AI Keywords**: text, ai, llm, prompt, model

---

#### `ai_tools/literal_ai.py`

**Description**: $id_{id}: String!
            $threadId_{id}: String
            $rootRunId_{id}: String
            $type_{id}: StepType
            $startTime_{id}: DateTime
            $endTime_{id}: DateTime
    ...

**Key Classes**: LiteralAILogger

**AI Keywords**: completion, text, generation, ai, llm, prompt, model

---

#### `ai_tools/params.py`

**AI Keywords**: completion, text, prompt, model

---

#### `ai_tools/pchart.py`

**Description**: Classes and interfaces for associating probabilities with tree
structures that represent the internal organization of a text.  The
probabilistic parser module defines ``BottomUpProbabilisticChartParse...

**Key Classes**: ProbabilisticLeafEdge, ProbabilisticTreeEdge, ProbabilisticBottomUpInitRule, ProbabilisticBottomUpPredictRule, ProbabilisticFundamentalRule

**AI Keywords**: text, ai, prompt

---

#### `ai_tools/budget_manager.py`

**Description**: duration needs to be one of ["daily", "weekly", "monthly", "yearly"]...

**Key Classes**: BudgetManager

**AI Keywords**: completion, text, ai, chat, llm, prompt, model

---

#### `ai_tools/writer_agent.py`

**Description**: A short 2-3 sentence summary of the findings....

**Key Classes**: ReportData

**AI Keywords**: ai, prompt, model

---

#### `ai_tools/session_group.py`

**Description**: SessionGroup concurrently manages multiple MCP session connections.

Tools, resources, and prompts are aggregated across servers. Servers may
be connected to or disconnected from at any point after in...

**Key Classes**: SseServerParameters, StreamableHttpParameters, ClientSessionGroup

**AI Keywords**: completion, text, ai, prompt, model

---

#### `ai_tools/patch_stdout.py`

**Description**: patch_stdout
============

This implements a context manager that ensures that print statements within
it won't destroy the user interface. The context manager will replace
`sys.stdout` by something t...

**Key Classes**: _Done, StdoutProxy

**AI Keywords**: text, ai, aws, prompt

---

#### `ai_tools/image.py`

**Key Classes**: CLIImageCreateArgs, CLIImageCreateVariationArgs, CLIImageEditArgs, CLIImage

**AI Keywords**: image, prompt, model

---

#### `ai_tools/activator.py`

**Description**: Generates activate script for the virtual environment....

**Key Classes**: Activator

**AI Keywords**: ai, prompt

---

#### `ai_tools/toolbars.py`

**Description**: Toolbar for a system prompt.

    :param prompt: Prompt to be displayed to the user....

**Key Classes**: FormattedTextToolbar, SystemToolbar, ArgToolbar, SearchToolbar, _CompletionsToolbarControl

**AI Keywords**: completion, text, ai, prompt

---

#### `ai_tools/_cli_hacks.py`

**Description**: Patch anyio.open_process to allow detached processes on Windows and Unix-like systems.

    This is necessary to prevent the MCP client from being interrupted by Ctrl+C when running in the CLI....

**AI Keywords**: text, ai, prompt

---

*... and 143 more modules in this category*


### Cloud AI Services (122 modules)

#### `ai_tools/regular.py`

**Description**: Functions for computing and verifying regular graphs....

**AI Keywords**: vertex, ai

---

#### `ai_tools/_tripcolor.py`

**Description**: Create a pseudocolor plot of an unstructured triangular grid.

    Call signatures::

      tripcolor(triangulation, c, *, ...)
      tripcolor(x, y, c, *, [triangles=triangles], [mask=mask], ...)

  ...

**AI Keywords**: vertex, ai

---

#### `ai_tools/line.py`

**Description**: Functions for generating line graphs....

**AI Keywords**: text, vertex, ai, bert

---

#### `ai_tools/test_similarity.py`

**Description**: G2 has edge (a,b) and G3 has edge (a,a) but node order for G2 is (a,b)
        while for G3 it is (b,a)...

**Key Classes**: TestSimilarity

**AI Keywords**: vertex, ai

---

#### `ai_tools/test_convert_numpy.py`

**Description**: Conversion from digraph to array to digraph....

**Key Classes**: TestConvertNumpyArray

**AI Keywords**: vertex, ai

---

#### `ai_tools/closeness.py`

**Description**: Closeness centrality measures....

**AI Keywords**: vertex, ai

---

#### `ai_tools/s3client.py`

**Description**: Client class for AWS S3 which handles authentication with AWS for [`S3Path`](../s3path/)
    instances. See documentation for the [`__init__` method][cloudpathlib.s3.s3client.S3Client.__init__]
    fo...

**Key Classes**: S3Client

**AI Keywords**: amazon, ai, ml, aws

---

#### `ai_tools/remote_storage.py`

**Description**: Push and pull outputs to and from a remote file storage.

    Remotes can be anything that `smart_open` can support: AWS, GCS, file system,
    ssh, etc....

**Key Classes**: RemoteStorage

**AI Keywords**: text, ai, aws, spacy

---

#### `ai_tools/connector.py`

**Description**: Wait for all waiters to finish closing....

**Key Classes**: _DeprecationWaiter, Connection, _ConnectTunnelConnection, _TransportPlaceholder, BaseConnector

**AI Keywords**: text, ai, ml, aws

---

#### `ai_tools/structs.py`

**Description**: Resolution state in a round....

**Key Classes**: DirectedGraph, IteratorMapping, _FactoryIterableView, _SequenceIterableView

**AI Keywords**: vertex, ai

---

#### `ai_tools/cographs.py`

**Description**: Generators for cographs

A cograph is a graph containing no path on four vertices.
Cographs or $P_4$-free graphs can be obtained from a single vertex
by disjoint union and complementation operations.
...

**AI Keywords**: generation, vertex, ai

---

#### `ai_tools/dag.py`

**Description**: Algorithms for directed acyclic graphs (DAGs).

Note that most of these functions are only guaranteed to work for DAGs.
In general, these functions do not check for acyclic-ness, so it is up
to the us...

**AI Keywords**: generation, vertex, ai, model

---

#### `ai_tools/base_secret_manager.py`

**Description**: Abstract base class for secret management implementations....

**Key Classes**: BaseSecretManager

**AI Keywords**: text, ai, llm, aws

---

#### `ai_tools/product.py`

**Description**: Graph products....

**AI Keywords**: vertex, ai, ml

---

#### `ai_tools/euler.py`

**Description**: Eulerian circuits and graphs....

**AI Keywords**: vertex, ai, ml

---

#### `ai_tools/dinitz_alg.py`

**Description**: Dinitz' algorithm for maximum flow problems....

**AI Keywords**: vertex, ai

---

#### `ai_tools/load_config_utils.py`

**Description**: Download a Python file from S3 and save it to local filesystem.
    
    Args:
        bucket_name (str): S3 bucket name
        object_key (str): S3 object key (file path in bucket)
        local_fil...

**AI Keywords**: completion, ai, ml, chat, llm, aws, bedrock

---

#### `ai_tools/test_connectivity.py`

**Key Classes**: TestAllPairsNodeConnectivity

**AI Keywords**: vertex, ai

---

#### `ai_tools/similarity.py`

**Description**: Functions measuring similarity using graph edit distance.

The graph edit distance is the number of edge/node changes needed
to make two graphs isomorphic.

The default algorithm/implementation is sub...

**AI Keywords**: text, generation, vertex, ai, ml

---

#### `ai_tools/push.py`

**Description**: Persist outputs to a remote storage. You can alias remotes in your
    project.yml by mapping them to storage paths. A storage can be anything that
    the smart_open library can upload to, e.g. AWS, ...

**AI Keywords**: ai, ml, aws, google

---

*... and 102 more modules in this category*


## Usage Guidelines

### For Contributors

1. **Import Standards**: Always use standard library imports as shown above
2. **Naming Conventions**: Use descriptive, non-conflicting module names
3. **Documentation**: Include comprehensive docstrings for all AI-related functions
4. **Testing**: Ensure all AI modules have appropriate test coverage

### For Users

1. **Local Processing**: All modules prioritize local-only processing for privacy
2. **API Keys**: Store API keys in environment variables, never in code
3. **Error Handling**: All modules include robust error handling and fallbacks
4. **Performance**: Modules are optimized for efficient AI workflows

## Integration Examples

### Basic LLM Usage
```python
from ai_tools.openai_handler import OpenAIHandler

handler = OpenAIHandler()
response = handler.complete("Your prompt here")
print(response)
```

### Embedding Generation
```python
from ai_tools.embedding_handler import EmbeddingHandler

embedder = EmbeddingHandler()
vector = embedder.embed_text("Text to embed")
```

### AI Safety & Guardrails
```python
from ai_tools.guardrails import ContentModerator

moderator = ContentModerator()
is_safe = moderator.check_content("User input")
```

## Repository Structure

```
ai-script-inventory/
├── ai/                          # Core AI modules (intent recognition, etc.)
├── ai_tools/                    # Main AI tooling directory (1000+ modules)
│   ├── ai_types/               # Renamed from types_mod (avoiding conflicts)
│   ├── pydantic_types.py       # Renamed from types_mod.py
│   └── [various AI modules]
├── ai_orchestra_project/        # AI orchestration and workflow management
├── python_scripts/             # Python scripts for AI tasks
├── typing_aliases.py           # Renamed from typing_mod.py
├── custom_enums.py            # Renamed from enum_mod_custom.py
└── superhuman_terminal.py     # AI-powered terminal interface
```

## Contributing

When adding new AI modules:

1. Place them in the appropriate directory (`ai_tools/` for general tools)
2. Use standard library imports only
3. Include comprehensive documentation
4. Add appropriate test coverage
5. Follow the established naming conventions

## Privacy & Security

All AI modules in this repository are designed with privacy in mind:

- **Local Processing**: No cloud dependencies unless explicitly required
- **Data Protection**: User data stays on local machine by default
- **API Security**: Secure handling of API keys and credentials
- **Audit Trails**: Comprehensive logging for debugging and compliance

---

*This documentation is automatically generated. Last updated: 2025-08-30 00:19:29*
