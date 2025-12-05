from app.states.blogstate import BlogState
from langchain_core.messages import HumanMessage
from app.states.blogstate import Blog

class BlogNode:
    def __init__(self, llm):
        self.llm = llm

    def title_creation(self, state: BlogState):
        if "topic" in state and state["topic"]:
            prompt = (
                "\n                   You are an expert blog content writer. Use Markdown formatting. Generate\n"
                "                   a blog title for the {topic}. This title should be creative and SEO friendly\n\n"
            )
            system_message = prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog": {"title": response.content}}

    def content_generation(self, state: BlogState):
        if "topic" in state and state["topic"]:
            system_prompt = (
                "You are expert blog writer. Use Markdown formatting.\n"
                "            Generate a detailed blog content with detailed breakdown for the {topic}"
            )
            system_message = system_prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog": {"title": state['blog']['title'], "content": response.content}}

    def translation(self, state: BlogState):
        translation_prompt = (
            "\n        Translate the following content into {current_language}.\n"
            "        - Maintain the original tone, style, and formatting.\n"
            "        - Adapt cultural references and idioms to be appropriate for {current_language}.\n\n"
            "        ORIGINAL CONTENT:\n        {blog_content}\n\n"
        )
        blog_content = state["blog"]["content"]
        messages = [
            HumanMessage(translation_prompt.format(current_language=state["current_language"], blog_content=blog_content))
        ]
        translation_content = self.llm.with_structured_output(Blog).invoke(messages)
        return {"blog": {"title": state["blog"]["title"], "content": translation_content.content}}

    def route(self, state: BlogState):
        return {"current_language": state['current_language']}

    def route_decision(self, state: BlogState):
        if state["current_language"] == "hindi":
            return "hindi"
        elif state["current_language"] == "french":
            return "french"
        else:
            return state['current_language']
