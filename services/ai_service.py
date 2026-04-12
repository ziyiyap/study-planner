import ollama
from config import OLLAMA_MODEL
from services.scoring_service import calculate_priority
from datetime import date

def call_llm(system_prompt, user_prompt):
    response = ollama.chat(
        model = OLLAMA_MODEL,
        messages= [
            {"role": "system", "content" : system_prompt},
            {"role" : "user", "content" : user_prompt}
        ]
    )

    return response.message.content

def summarize_chunk(chunk):
    system_prompt = (
        "You are an academic study material summarizer. "
        "Summarize the following study material into concise key concepts and important points. "
        "Focus only on academic content. "
        "Ignore any formatting artifacts or incomplete sentences. "
        "Respond in clear, plain English. "
        "Do not include any preamble or explanation — only the summary."
    )
    summary = call_llm(system_prompt, chunk)

    return summary

def summarize_pdf(chunks):
    summarized_chunks = []
    for chunk in chunks:
       summarized_chunks.append(summarize_chunk(chunk))

    
    system_prompt = (
        "You are an academic study material summarizer. "
        "You will receive multiple summaries of different sections of the same document. "
        "Combine them into one cohesive, concise summary covering all key concepts. "
        "Do not repeat information. "
        "Respond in plain English with no preamble."
    )

    overall_summary = call_llm(system_prompt, "\n\n".join(summarized_chunks))
    return overall_summary

def analyze_difficulty(summary, doc_type):
    #follow agent_1, agent_2, agent_3
    math_doc = [0.5, 0.3, 0.2]
    text_doc = [0.2, 0.3, 0.5]
    agent_1 = (
        "You are an academic difficulty analyzer specializing in mathematical and technical complexity. "
        "Analyze the provided study material summary and rate its mathematical and technical difficulty. "
        "Consider the complexity of formulas, equations, and technical procedures. "
        "Respond with only a single decimal number between 0.0 and 1.0. No explanation, no text, just the number."
    )

    agent_2 = (
        "You are an academic difficulty analyzer specializing in conceptual density and abstraction. "
        "Analyze the provided study material summary and rate how conceptually dense and abstract it is. "
        "Consider the depth of theory, interconnected concepts, and level of abstract thinking required. "
        "Respond with only a single decimal number between 0.0 and 1.0. No explanation, no text, just the number."
    )

    agent_3 = (
        "You are an academic difficulty analyzer specializing in vocabulary and assumed prior knowledge. "
        "Analyze the provided study material summary and rate how much prior knowledge and technical vocabulary is assumed. "
        "Consider the complexity of terminology and prerequisite knowledge required to understand the material. "
        "Respond with only a single decimal number between 0.0 and 1.0. No explanation, no text, just the number."
    )

    rate_list = [float(n) for n in [call_llm(agent_1, summary), call_llm(agent_2, summary), call_llm(agent_3, summary)]]
    
    score = 0
    if doc_type == "math":
        for i in range(len(math_doc)):
            score += rate_list[i] * math_doc[i]
    elif doc_type == "text":
        for i in range(len(text_doc)):
            score += rate_list[i] * text_doc[i]

    return score

def generate_insights(subjects): #list of objects
    system_prompt = (
            "You are a personal study advisor analyzing a student's current academic situation. "
            "You will receive data about the student's subjects including deadlines, progress, difficulty, passion, and importance. "
            "Provide specific, actionable study recommendations based on urgency, difficulty, and the student's passion levels. "
            "Prioritize subjects with approaching deadlines and low progress. "
            "Consider passion level when making recommendations — low passion subjects may need motivational strategies. "
            "Be concise, direct, and practical. "
            "Respond in clear plain English with no preamble."
        )
    
    user_prompt = ""
    for subject in subjects: #subject is an object
        user_prompt += (
            f"Subject: {subject.name}\n"
            f"Exam in: {(subject.exam_date - date.today()).days} day(s)\n"
            f"Progress: {subject.progress * 100}%\n"
            f"Priority score: {calculate_priority(subject)}\n"
            f"Difficulty: {subject.effective_difficulty}\n"
            f"Passion level: {subject.passion_level}\n"
            f"Importance: {subject.importance_weight}\n"
            "\n\n"
        )

    response = call_llm(system_prompt, user_prompt)
    return response