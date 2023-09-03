from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from api import llm
from langchain.output_parsers import ResponseSchema, StructuredOutputParser ,RetryOutputParser
from langchain.callbacks.streaming_stdout_final_only import FinalStreamingStdOutCallbackHandler
from langchain.prompts import PromptTemplate



def summarize(text):
    # Number of sentences in the summary
    summary_sentences_count = 4
    # Initialize the summarizer
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LexRankSummarizer()

    # Generate the summary
    summary = summarizer(parser.document, summary_sentences_count)
    summary_sentences_output = [str(sentence) for sentence in summary]
    summary_sentences = " ".join(summary_sentences_output)
    return summary_sentences

def summarize_llm(text):
    summary_length = (len(text.split(" ")) * 50)//100
    response_schema = [ResponseSchema(name="curate", description="curate the provided text")]
    output_parser = StructuredOutputParser.from_response_schemas(response_schema)
    format_instruction = output_parser.get_format_instructions()
    prompt = PromptTemplate(
        template="text : '{text}' . curate the text in {summary_length} words, {format_instruction}",
        input_variables=["text","summary_length"],
        partial_variables={"format_instruction": format_instruction}
    )
    _input = prompt.format_prompt(text=text , summary_length=summary_length)
    output = llm(_input.to_string())
    try :
        summary = output_parser.parse(output)['curate']
    except :
        summary = output.split('"curate":')[-1].replace("}"," ").replace("```"," ").strip()
    return summary
  


    