# gptpdf-LaTeX

This is a fork of the [gptpdf](https://github.com/CosmosShadow/gptpdf) repository. Instead of using markdown, the LLM will output LaTeX code.
Using VLLM (like GPT-4o) to parse PDF into LaTeX format.

This tool now features a new YOLO-based figure detection system that significantly improves the accuracy of figure extraction. This is now the recommended way to use the tool, though backward compatibility with the original method is maintained.

Our approach can almost perfectly parse typography, math formulas, tables, pictures, charts, etc. With the new YOLO-based figure detection, the accuracy of figure extraction is significantly improved.

Average cost per page: $0.013

This package uses [GeneralAgent](https://github.com/CosmosShadow/GeneralAgent) library to interact with OpenAI API and [DocLayout-YOLOv10](https://github.com/opendatalab/DocLayout-YOLO) for figure detection.

[pdfgpt-ui](https://github.com/daodao97/gptpdf-ui) is a visual tool based on gptpdf.

## Installation

### Requirements
- Python 3.8.1 or higher
- OpenAI API key for GPT-4o or other compatible models
- CUDA-capable GPU (optional, but recommended for faster YOLO inference)
  - Install [CUDA Toolkit](https://developer.nvidia.com/cuda-downloads)
- Torch
  - Install torch for the same cuda version or for CPU https://pytorch.org/get-started/locally/

### Installation with pip

```bash
# Clone the repository
git clone https://github.com/CosmosShadow/gptpdf.git
cd gptpdf

# Install the package and its dependencies
pip install -e .
```

### Installation with Poetry

```bash
# Clone the repository
git clone https://github.com/CosmosShadow/gptpdf.git
cd gptpdf

# Install dependencies with Poetry
poetry install
```

### Key Dependencies
- **GeneralAgent**: For interacting with OpenAI API
- **PyMuPDF**: For parsing PDF files
- **DocLayout-YOLOv10**: For figure detection
- **torch**: For running the YOLO model
- **matplotlib**: For visualizing and saving figures
- **huggingface-hub**: For downloading pre-trained YOLO models


## Process steps

### New Method with YOLO (Recommended)
1. Use the PyMuPDF library to parse the PDF into images
2. Use YOLOv10 to detect figures, pictures, or graphs in the images
3. Create annotated images with only figure boundaries marked
4. Use a large visual model (such as GPT-4o) to parse text content only
5. Extract and crop the detected figures
6. Combine the text content with the extracted figures in the final LaTeX document

The YOLO-based method provides more accurate figure detection and better handling of complex layouts. It is now the recommended approach, but the original method is still supported for backward compatibility.

### Original Method (Legacy)
1. Use the PyMuPDF library to parse the PDF to find all non-text areas and mark them, for example:

![](docs/demo.jpg)

2. Use a large visual model (such as GPT-4o) to parse and extract both text and images.



## Usage

### Local Usage

```python
from gptpdf import parse_pdf
api_key = 'Your OpenAI API Key'
content, image_paths = parse_pdf(pdf_path, api_key=api_key)
print(content)
```

See more in [examples/PDF_to_LaTeX.py](examples/PDF_to_LaTeX.py)


## API

### parse_pdf

**Function**: 
```
def parse_pdf(
        pdf_path: str,
        output_dir: str = './',
        prompt: Optional[Dict] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: str = 'gpt-4o',
        verbose: bool = False,
        gpt_worker: int = 1,
        document_initial_text: str = '',
        document_final_text: str = '',
        output_dir_images: Optional[str] = None,
        cleanup_unused: bool = True,
        use_sequential_naming: bool = False,
        use_yolo_detector: bool = True,
        yolo_device: Optional[str] = None
) -> Tuple[str, List[str]]:
```

Parses a PDF file into LaTeX format and returns the LaTeX content along with all image paths.

**Parameters**:

- **pdf_path**: *str*  
  Path to the PDF file

- **output_dir**: *str*, default: './'  
  Output directory to store all images and the Markdown file

- **api_key**: *Optional[str]*, optional  
  OpenAI API key. If not provided, the `OPENAI_API_KEY` environment variable will be used.

- **base_url**: *Optional[str]*, optional  
  OpenAI base URL. If not provided, the `OPENAI_BASE_URL` environment variable will be used. This can be modified to call other large model services with OpenAI API interfaces, such as `GLM-4V`.

- **model**: *str*, default: 'gpt-4o'  
  OpenAI API formatted multimodal large model. If you need to use other models, such as:
  - [qwen-vl-max](https://help.aliyun.com/zh/dashscope/developer-reference/compatibility-of-openai-with-dashscope) 
  - [GLM-4V](https://open.bigmodel.cn/dev/api#glm-4v)
  - [Yi-Vision](https://platform.lingyiwanwu.com/docs) 
  - Azure OpenAI, by setting the `base_url` to `https://xxxx.openai.azure.com/` to use Azure OpenAI, where `api_key` is the Azure API key, and the model is similar to `azure_xxxx`, where `xxxx` is the deployed model name (tested).

- **verbose**: *bool*, default: False  
  Verbose mode. When enabled, the content parsed by the large model will be displayed in the command line.

- **gpt_worker**: *int*, default: 1  
  Number of GPT parsing worker threads. If your machine has better performance, you can increase this value to speed up the parsing.

- **prompt**: *dict*, optional  
  If the model you are using does not match the default prompt provided in this repository and cannot achieve the best results, we support adding custom prompts. The prompts in the repository are divided into three parts:
  - `prompt`: Mainly used to guide the model on how to process and convert text content in images.
  - `rect_prompt`: Used to handle cases where specific areas (such as tables or images) are marked in the image.
  - `role_prompt`: Defines the role of the model to ensure the model understands it is performing a PDF document parsing task.

- **document_initial_text**: *str*, default: ''
    Initial text to be added to the document before the outputted content.
- **document_final_text**: *str*, default: ''  
  Final text to be added to the document after the outputted content.

- **output_dir_images**: *Optional[str]*, default: None  
  Path to the output directory for images. If not provided, images will be stored in a subdirectory named "images" under the output_dir.

- **cleanup_unused**: *bool*, default: True  
  Whether to clean up unused images, page images, and annotated images after processing.

- **use_sequential_naming**: *bool*, default: False  
  Whether to use sequential naming for images (image1.png, image2.png, etc.) instead of page-based naming.

- **use_yolo_detector**: *bool*, default: True  
  Whether to use the YOLO detector for figure detection (recommended). When set to True, the LLM will only process text content, and figures will be detected and extracted using YOLOv10. When set to False, the original method will be used where the LLM processes both text and images.

- **yolo_device**: *Optional[str]*, default: None  
  Device to use for YOLO inference ('cuda:0' or 'cpu'). If not provided, will use CUDA if available, otherwise CPU.

  You can pass custom prompts in the form of a dictionary to replace any of the prompts. Here is an example:

```
prompt = {
    "prompt": "Custom prompt text",
    "rect_prompt": "Custom rect prompt",
    "role_prompt": "Custom role prompt"
}

content, image_paths = parse_pdf(
    pdf_path=pdf_path,
    output_dir='./output',
    model="gpt-4o",
    prompt=prompt,
    verbose=False,
)
```



**args**: LLM other parameters, such as `temperature`, `top_p`, `max_tokens`, `presence_penalty`, `frequency_penalty`, etc.
