#!/usr/bin/env python3
"""
Resume and Cover Letter Reviewer - Llama-Based Career Tool
Provides feedback on job application materials
Author: Pranay M
"""

import ollama
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.markdown import Markdown
import json

console = Console()

INDUSTRIES = ["Technology", "Healthcare", "Finance", "Education", "Marketing",
              "Engineering", "Legal", "Government", "Non-profit", "Consulting"]

EXPERIENCE_LEVELS = ["Entry-level", "Mid-level", "Senior", "Executive", "Career Change"]


class ResumeReviewer:
    def __init__(self, model: str = "llama3.2"):
        self.model = model
    
    def review_resume(self, resume_text: str, job_title: str = "", industry: str = "") -> dict:
        prompt = f"""Review this resume and provide detailed feedback.

Resume:
{resume_text}

Target Job: {job_title if job_title else "General"}
Industry: {industry if industry else "General"}

Return JSON:
{{
    "overall_score": 75,
    "overall_assessment": "summary assessment",
    "section_reviews": {{
        "contact_info": {{
            "score": 90,
            "feedback": "assessment",
            "suggestions": ["improvements"]
        }},
        "summary_objective": {{
            "score": 70,
            "feedback": "assessment",
            "suggestions": ["improvements"]
        }},
        "experience": {{
            "score": 75,
            "feedback": "assessment",
            "bullet_point_quality": "assessment",
            "action_verbs_used": true,
            "quantified_achievements": false,
            "suggestions": ["improvements"]
        }},
        "education": {{
            "score": 80,
            "feedback": "assessment",
            "suggestions": ["improvements"]
        }},
        "skills": {{
            "score": 70,
            "feedback": "assessment",
            "missing_skills": ["skills to add"],
            "suggestions": ["improvements"]
        }}
    }},
    "ats_compatibility": {{
        "score": 65,
        "issues": ["ATS problems found"],
        "recommendations": ["how to fix"]
    }},
    "formatting": {{
        "score": 80,
        "issues": ["formatting problems"],
        "recommendations": ["fixes"]
    }},
    "language_quality": {{
        "grammar_issues": ["errors found"],
        "weak_phrases": ["phrases to improve"],
        "strong_phrases": ["good phrases to keep"]
    }},
    "keyword_analysis": {{
        "relevant_keywords": ["keywords found"],
        "missing_keywords": ["keywords to add"],
        "keyword_density": "assessment"
    }},
    "top_3_improvements": ["most important changes"],
    "strengths": ["what's working well"]
}}"""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return self._parse_json(response['message']['content'])
    
    def review_cover_letter(self, cover_letter: str, job_description: str = "") -> dict:
        prompt = f"""Review this cover letter and provide feedback.

Cover Letter:
{cover_letter}

Job Description (if provided):
{job_description if job_description else "Not provided"}

Return JSON:
{{
    "overall_score": 75,
    "overall_assessment": "summary",
    "structure_review": {{
        "opening": {{
            "score": 70,
            "has_hook": true,
            "mentions_position": true,
            "feedback": "assessment"
        }},
        "body": {{
            "score": 75,
            "shows_fit": true,
            "specific_examples": true,
            "addresses_requirements": true,
            "feedback": "assessment"
        }},
        "closing": {{
            "score": 80,
            "call_to_action": true,
            "professional_tone": true,
            "feedback": "assessment"
        }}
    }},
    "content_analysis": {{
        "relevance_to_job": "high/medium/low",
        "unique_value_proposition": "assessment",
        "company_research_shown": true,
        "enthusiasm_conveyed": true
    }},
    "tone_and_voice": {{
        "professionalism": "assessment",
        "confidence_level": "assessment",
        "authenticity": "assessment"
    }},
    "improvements_needed": [
        {{
            "issue": "problem",
            "current": "what's there",
            "suggested": "what to write instead"
        }}
    ],
    "strengths": ["what works well"],
    "rewritten_opening": "suggested better opening paragraph",
    "rewritten_closing": "suggested better closing paragraph"
}}"""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return self._parse_json(response['message']['content'])
    
    def optimize_for_job(self, resume_text: str, job_description: str) -> dict:
        prompt = f"""Optimize this resume for the specific job posting.

Resume:
{resume_text}

Job Description:
{job_description}

Return JSON:
{{
    "match_score": 70,
    "keyword_matches": ["matching keywords"],
    "missing_requirements": ["requirements not shown on resume"],
    "transferable_skills": ["skills that could apply"],
    "optimization_suggestions": [
        {{
            "section": "which section",
            "current": "current content",
            "optimized": "improved version",
            "rationale": "why this change helps"
        }}
    ],
    "experience_to_highlight": ["experiences to emphasize"],
    "experience_to_minimize": ["less relevant experiences"],
    "skills_to_add": ["skills to include"],
    "achievements_to_quantify": ["achievements that need numbers"],
    "tailored_summary": "customized summary/objective statement",
    "priority_changes": ["most important modifications"]
}}"""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return self._parse_json(response['message']['content'])
    
    def generate_bullet_points(self, job_title: str, responsibilities: str) -> dict:
        prompt = f"""Generate strong resume bullet points.

Job Title: {job_title}
Responsibilities/Achievements: {responsibilities}

Return JSON:
{{
    "bullet_points": [
        {{
            "bullet": "strong action-oriented bullet point",
            "action_verb": "verb used",
            "quantification": "numbers included",
            "impact_shown": true
        }}
    ],
    "alternative_verbs": ["powerful action verbs to consider"],
    "quantification_tips": ["how to add numbers"],
    "impact_phrases": ["ways to show results"]
}}"""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return self._parse_json(response['message']['content'])
    
    def generate_cover_letter(self, resume_summary: str, job_description: str, 
                             company: str) -> dict:
        prompt = f"""Generate a cover letter draft.

Background: {resume_summary}
Job Description: {job_description}
Company: {company}

Return JSON:
{{
    "cover_letter": {{
        "opening_paragraph": "engaging opening",
        "body_paragraph_1": "relevant experience and skills",
        "body_paragraph_2": "why this company/role",
        "closing_paragraph": "call to action and thank you"
    }},
    "full_letter": "complete cover letter text",
    "customization_notes": ["how to personalize further"],
    "alternative_openings": ["other opening options"],
    "key_points_included": ["main selling points covered"]
}}"""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return self._parse_json(response['message']['content'])
    
    def _parse_json(self, content: str) -> dict:
        try:
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end > start:
                return json.loads(content[start:end])
        except:
            pass
        return {"raw_response": content}


def display_menu():
    table = Table(title="📄 Resume & Cover Letter Reviewer", show_header=True)
    table.add_column("Option", style="cyan", width=6)
    table.add_column("Feature", style="green")
    table.add_column("Description", style="white")
    
    table.add_row("1", "Review Resume", "Get resume feedback")
    table.add_row("2", "Review Cover Letter", "Get cover letter feedback")
    table.add_row("3", "Optimize for Job", "Tailor resume to job")
    table.add_row("4", "Generate Bullets", "Create strong bullet points")
    table.add_row("5", "Generate Cover Letter", "Draft a cover letter")
    table.add_row("0", "Exit", "Close application")
    
    console.print(table)


def main():
    console.print(Panel.fit(
        "[bold blue]📄 Resume & Cover Letter Reviewer[/bold blue]\n"
        "[green]AI-Powered Job Application Feedback[/green]\n"
        "[dim]Author: Pranay M[/dim]",
        border_style="blue"
    ))
    
    reviewer = ResumeReviewer()
    
    while True:
        display_menu()
        choice = Prompt.ask("\n[cyan]Select option[/cyan]", default="0")
        
        if choice == "0":
            console.print("[yellow]Goodbye! Land that dream job! 📄[/yellow]")
            break
        
        with console.status("[bold green]Analyzing..."):
            if choice == "1":
                console.print("[dim]Paste resume text (end with 'EOF'):[/dim]")
                lines = []
                while True:
                    line = input()
                    if line.strip() == "EOF":
                        break
                    lines.append(line)
                job_title = Prompt.ask("Target job title (optional)", default="")
                industry = Prompt.ask("Industry (optional)", default="")
                result = reviewer.review_resume("\n".join(lines), job_title, industry)
                console.print(Panel(Markdown(f"```json\n{json.dumps(result, indent=2)}\n```"),
                                   title="📊 Resume Review"))
            
            elif choice == "2":
                console.print("[dim]Paste cover letter (end with 'EOF'):[/dim]")
                lines = []
                while True:
                    line = input()
                    if line.strip() == "EOF":
                        break
                    lines.append(line)
                job_desc = Prompt.ask("Job description (optional)", default="")
                result = reviewer.review_cover_letter("\n".join(lines), job_desc)
                console.print(Panel(Markdown(f"```json\n{json.dumps(result, indent=2)}\n```"),
                                   title="📊 Cover Letter Review"))
            
            elif choice == "3":
                console.print("[dim]Paste resume (end with 'EOF'):[/dim]")
                resume_lines = []
                while True:
                    line = input()
                    if line.strip() == "EOF":
                        break
                    resume_lines.append(line)
                console.print("[dim]Paste job description (end with 'EOF'):[/dim]")
                job_lines = []
                while True:
                    line = input()
                    if line.strip() == "EOF":
                        break
                    job_lines.append(line)
                result = reviewer.optimize_for_job("\n".join(resume_lines), "\n".join(job_lines))
                console.print(Panel(Markdown(f"```json\n{json.dumps(result, indent=2)}\n```"),
                                   title="🎯 Optimization Suggestions"))
            
            elif choice == "4":
                job_title = Prompt.ask("Job title")
                responsibilities = Prompt.ask("Describe responsibilities/achievements")
                result = reviewer.generate_bullet_points(job_title, responsibilities)
                console.print(Panel(Markdown(f"```json\n{json.dumps(result, indent=2)}\n```"),
                                   title="✓ Bullet Points"))
            
            elif choice == "5":
                summary = Prompt.ask("Summarize your background")
                job_desc = Prompt.ask("Job description/requirements")
                company = Prompt.ask("Company name")
                result = reviewer.generate_cover_letter(summary, job_desc, company)
                console.print(Panel(Markdown(f"```json\n{json.dumps(result, indent=2)}\n```"),
                                   title="✉️ Cover Letter Draft"))
        
        console.print("\n" + "="*50)


if __name__ == "__main__":
    main()
