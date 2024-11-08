import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import re
import PyPDF2
from docx import Document
from PIL import Image, ImageTk

class DigitalGuardianApp:
    def __init__(self, master):
        self.master = master
        master.title("Digital Guardian")
        master.geometry("600x500")  # Set window size
        self.set_background()  # Call the background setting method
        self.create_widgets()

    def set_background(self):
        # Load an image and set it as the background
        self.bg_image = Image.open(r"E:\Digital Guardian\background.png")  # Ensure the image path is correct
        self.bg_image = self.bg_image.resize((600, 500), Image.LANCZOS)  # Use LANCZOS for better quality
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create a label to hold the background image
        self.bg_label = tk.Label(self.master, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def create_widgets(self):
        # Title Label
        title_label = tk.Label(self.master, text="Digital Guardian", font=("Arial", 20, "bold"), bg="#f0f0f0")
        title_label.pack(pady=10)

        # Instructions Label
        instructions_label = tk.Label(self.master, text="Upload your CV (PDF or Word):", bg="#f0f0f0")
        instructions_label.pack(pady=5)

        # Country Selection
        self.country_var = tk.StringVar()
        country_label = tk.Label(self.master, text="Select Country:", bg="#f0f0f0")
        country_label.pack(pady=5)
        country_options = ["Egypt", "Russia", "England", "Canada", "Saudi Arabia", "USA"]
        self.country_menu = tk.OptionMenu(self.master, self.country_var, *country_options)
        self.country_menu.pack(pady=5)

        # File Upload Button
        self.upload_button = tk.Button(self.master, text="Upload CV", command=self.upload_cv, bg="#007bff", fg="white")
        self.upload_button.pack(pady=20)

        # Exam Button
        self.exam_button = tk.Button(self.master, text="Take Exam", command=self.take_exam, bg="#28a745", fg="white")
        self.exam_button.pack(pady=10)

        # Quit Button
        self.quit_button = tk.Button(self.master, text="Quit", command=self.master.quit, bg="#dc3545", fg="white")
        self.quit_button.pack(pady=5)

        # Requirements Dictionary
        self.requirements = {
            "Egypt": {
                "experience": "3 years SOC",
                "education": "Bachelor's or Master's in IT",
                "skills": ["Incident Management", "SIEM", "Threat Analysis"],
            },
            "Russia": {
                "experience": "3 years Cybersecurity",
                "education": "Information Security degree",
                "skills": ["UNIX Administration", "Scripting", "Network Security"],
            },
            "England": {
                "experience": "2 years SOC",
                "education": "IT degree",
                "skills": ["KQL", "OSINT", "SIEM"],
            },
            "Canada": {
                "experience": "3-5 years in Cybersecurity",
                "education": "Computer Science degree",
                "skills": ["Incident Response", "SIEM", "Threat Hunting"],
            },
            "Saudi Arabia": {
                "experience": "4 years Cybersecurity",
                "education": "IT-related degree",
                "skills": ["TCP/IP", "Security Tools", "Log Analysis"],
            },
            "USA": {
                "experience": "3 years IT Security",
                "education": "Cybersecurity degree",
                "skills": ["EDR", "SIEM", "Incident Response"],
            },
        }

    def upload_cv(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("Word files", "*.docx")])
        if file_path:
            user_data = self.extract_info_from_cv(file_path)
            if user_data:
                match_percentage = self.calculate_match_percentage(user_data)
                self.show_result(match_percentage)
            else:
                messagebox.showwarning("Error", "Could not extract information from the CV.")

    def extract_info_from_cv(self, file_path):
        try:
            if file_path.endswith('.pdf'):
                return self.extract_info_from_pdf(file_path)
            elif file_path.endswith('.docx'):
                return self.extract_info_from_word(file_path)
            else:
                messagebox.showwarning("Error", "Unsupported file format.")
                return None
        except Exception as e:
            messagebox.showwarning("Error", f"An error occurred: {e}")
            return None

    def extract_info_from_pdf(self, file_path):
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            content = ""
            for page in reader.pages:
                content += page.extract_text() + "\n"
        return self.parse_content(content)

    def extract_info_from_word(self, file_path):
        doc = Document(file_path)
        content = ""
        for para in doc.paragraphs:
            content += para.text + "\n"
        return self.parse_content(content)

    def parse_content(self, content):
        # Simple regex patterns to extract experience, education, and skills
        experience = re.search(r'Experience:\s*(.*)', content)
        education = re.search(r'Education:\s*(.*)', content)
        skills = re.search(r'Skills:\s*(.*)', content)

        user_data = {
            'experience': experience.group(1).strip() if experience else "",
            'education': education.group(1).strip() if education else "",
            'skills': skills.group(1).strip().split(',') if skills else [],
        }
        return user_data

    def calculate_match_percentage(self, user_data):
        match_percentage = 0
        total_requirements = len(self.requirements[self.country_var.get()])  # Only count for selected country

        # Get requirements for the selected country
        req = self.requirements[self.country_var.get()]

        # Check experience
        if user_data['experience'] in req['experience']:
            match_percentage += 1
        # Check education
        if user_data['education'] in req['education']:
            match_percentage += 1
        # Check skills
        skill_matches = sum(1 for skill in req['skills'] if skill.strip() in user_data['skills'])
        match_percentage += skill_matches / len(req['skills'])  # Weight by the number of skills

        match_percentage = (match_percentage / total_requirements) * 100  # Normalize to percentage
        return match_percentage

    def show_result(self, match_percentage):
        # Adjust eligibility criteria to 50%
        if match_percentage >= 50:
            messagebox.showinfo("Eligibility", "You are eligible for the exam!")
        else:
            messagebox.showwarning("Eligibility", "You are not eligible to take the exam because you did not meet the basic requirements.")

    def take_exam(self):
        exam_questions = self.get_exam_questions()
        answers = simpledialog.askstring("Exam", exam_questions)
        if answers:
            self.review_answers(answers)

    def review_answers(self, answers):
        # Here you can implement logic to review the answers against the requirements
        # For simplicity, we're just showing the answers entered
        messagebox.showinfo("Exam Answers", f"You answered:\n{answers}")

    def get_exam_questions(self):
        questions = {
            "easy": ["What is SIEM?", "Define Incident Response."],
            "intermediate": ["Explain the Cyber Kill Chain.", "What is the purpose of a firewall?"],
            "advanced": ["Describe the MITRE ATT&CK framework.", "How do you conduct a threat hunt?"],
        }
        
        exam_text = "Exam Questions:\n"
        for level, qs in questions.items():
            exam_text += f"\n{level.capitalize()} Questions:\n"
            for question in qs:
                exam_text += f"- {question}\n"
        return exam_text

if __name__ == "__main__":
    root = tk.Tk()
    app = DigitalGuardianApp(root)
    root.mainloop()