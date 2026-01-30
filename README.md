# AarogyaQueue

**"Because the sickest shouldn't wait the longest."**

Built in 24 hours for Central India Hackathon (CIH 3.0) | SDG 3: Good Health & Well-Being

---

## What Problem Are We Solving?

In rural India, government health centers often have just 1 or 2 doctors managing 100+ patients every day. Right now, these clinics use a simple first-come-first-serve system—whoever comes first, gets treated first.

**Why is this a problem?**

Imagine this: A patient with severe chest pain arrives at 10 AM. But there are already 40 people in line who came earlier, mostly with minor colds and fevers. That chest pain patient has to wait 3+ hours just because they came late.

**In healthcare, arrival time should not decide who gets treated first. Medical urgency should.**

But most clinics don't have the staff or tools to manually sort patients by urgency. That's where we come in.

---

## Our Idea .

AarogyaQueue is a simple queue management system that helps small clinics automatically prioritize patients based on how serious their symptoms are—not when they arrived.

Patients tell their symptoms (by voice or text), and our system gives them a risk score. High-risk patients go to the front of the line. Low-risk patients wait a bit longer. This way, critically ill people get faster care, and junior doctors can handle simple cases while senior doctors focus on serious ones.

**This is not a diagnosis tool.** We don't tell anyone what disease they have. We just help organize the waiting line better.

---

## How AarogyaQueue Works (Simple Flow)

Here's what happens when a patient visits a clinic using our system:

**Step 1: Patient Arrives**  
They enter their phone number and year of birth at a kiosk (tablet at the clinic entrance).

**Step 2: Describe Symptoms**  
The system asks: "What problem are you facing today?"  
The patient speaks or types their answer (e.g., "I have fever and cough for 3 days").

**Step 3: Computer Understands Symptoms**  
Our system uses AI to convert speech to text and extract important details like age, symptoms, and how long they've been sick.

**Step 4: Risk Score Is Calculated**  
A machine learning model (trained on medical data) gives the patient a risk score from 0 to 1.  
- **High risk (0.7–1.0)**: Serious symptoms like chest pain, breathing difficulty  
- **Medium risk (0.4–0.7)**: Persistent fever, severe headache  
- **Low risk (0–0.4)**: Mild cold, minor injuries

**Step 5: Patient Gets Token & Wait Time**  
The patient receives a token number and estimated wait time. They can see where they are in the queue.

**Step 6: Doctor Sees the Queue**  
Doctors log into their dashboard and select their role (Junior Doctor or Senior Doctor).  
- Senior doctors see high and medium-risk patients.  
- Junior doctors see low-risk patients.

**Step 7: Doctor Reviews Patient Summary**  
The doctor sees the patient's symptoms, risk score, and why they were flagged as urgent.

**Step 8: Consultation Happens**  
Doctor examines the patient, enters diagnosis, and clicks "Next Patient."

---

## What We Built in This Hackathon (MVP)

Here's what actually works right now after 24 hours of building:

### Patient Side (Kiosk Interface)
- Phone number and year of birth entry for quick registration
- Text input for symptoms (voice input is simulated—we didn't have time to fully integrate speech recognition)
- AI extracts structured data from free-text symptoms
- Displays token number, risk level, and queue position
- Shows estimated wait time

### Doctor Side (Dashboard)
- Doctor selects role: Junior or Senior
- Sees only relevant patients (based on risk score)
- Views patient cards with:
  - Token number
  - Risk badge (High/Medium/Low)
  - AI-generated symptom summary
- Enters diagnosis and submits
- Next patient automatically loads

### Behind the Scenes
- Custom machine learning model (Random Forest) calculates risk scores based on symptoms
- Database (Supabase) stores patient records and keeps queues updated in real-time
- Risk-based routing: Patients automatically go to the right queue

---

## Why This Is Useful in the Real World

## Why This Is Useful in the Real World

### For Clinics
- No extra staff needed to manually triage patients
- Works on a single tablet—minimal setup cost
- Reduces chaos and arguments in the waiting area (everyone sees why someone was prioritized)

### For Doctors
- Senior doctors spend time on serious cases, not routine checkups
- Junior doctors gain experience with low-risk cases without risking patient safety
- Patient summaries save 2–3 minutes per consultation (no need to re-ask all symptoms)

### For Patients
- Critical patients get faster care—potentially life-saving
- Transparent system shows your position and why you're waiting
- No need to download an app or create accounts—works immediately

**Real-world estimate:**  
In a clinic with 100 patients/day, this system could reduce average wait time for high-risk cases by 30–40 minutes and help doctors see 10–15% more patients in the same time.

---

## SDG Alignment & Social Impact

This project directly addresses **SDG 3: Good Health & Well-Being**, specifically:

- **Target 3.8 (Universal Health Coverage):** Makes existing rural clinics more efficient without requiring more doctors
- **Target 3.c (Health Workforce Optimization):** Helps available doctors serve more people safely

### Measurable Impact

If deployed in just 100 Primary Health Centers across rural India:
- **15,000+ patients prioritized daily** based on medical need, not arrival time
- **Potentially life-saving** for emergency cases that would otherwise wait hours
- **Reduced doctor burnout** by distributing workload intelligently

This is about **fairness in healthcare**—making sure limited resources go to those who need them most urgently.

---

## Technology Used (Very Brief)

We kept the tech stack simple so the project works reliably in a 24-hour demo:

- **Streamlit:** Quick web interface for both patient and doctor sides (chose it because we could build UI fast)
- **OpenAI API:** Converts symptoms into structured data (only for data extraction, not diagnosis)
- **scikit-learn (Random Forest):** Custom ML model for risk scoring (works offline, no internet needed after training)
- **Supabase:** Cloud database that syncs queues in real-time between patient and doctor apps
- **Python:** Backend logic and ML model training

**Why we didn't just use ChatGPT for everything:**  
Large language models can "hallucinate" or give inconsistent results. For something as serious as healthcare prioritization, we built a dedicated ML model trained on medical triage data. It's more reliable and we can explain exactly why a score was given.

---

## Limitations (Honest Section – VERY IMPORTANT)

We want to be very clear about what this system does NOT do:

### What We Did NOT Build
- **No actual voice recognition:** Right now, patients type their symptoms. Voice input would be added using speech-to-text APIs.
- **No real medical diagnosis:** This system only prioritizes—it doesn't tell anyone what disease they have.
- **No integration with hospital records:** Patient data is temporary (session-based).
- **No multi-language support yet:** Interface is in English (Hindi/regional languages would be added later).
- **No user authentication:** This is a demo—a real deployment would need secure logins.

### Hackathon Constraints We Acknowledge
- The ML model is trained on publicly available medical data, not real Indian PHC data (we didn't have access in 24 hours).
- We haven't tested this with real doctors or patients yet (that would be the next step).
- The system assumes one clinic—multi-clinic networks would need more work.

**This is an MVP (Minimum Viable Product), not a finished product ready for hospitals.**

---

## Future Improvements

If we continue working on this after the hackathon, here are the next steps:

1. **WhatsApp Integration:**  
   Patients could send a voice message to a WhatsApp number before reaching the clinic, reducing kiosk crowding.

2. **Real Voice Input in Local Languages:**  
   Add support for Hindi, Marathi, and other regional languages using Google Speech-to-Text or similar.

3. **Analytics Dashboard for Health Officials:**  
   Track disease patterns, peak hours, and clinic efficiency to help government allocate resources better (e.g., "Send an extra doctor to this PHC on Tuesdays").

---

## Team & Hackathon Context

This project was built from scratch in 24 hours by a team of 4 students at **Central India Hackathon (CIH 3.0)**.

We divided the work as:
- **Frontend development:** Patient and doctor interfaces
- **Backend & ML:** Risk scoring model and API
- **Data preparation:** Finding datasets and training the model
- **Integration:** Making everything work together

**What we learned:**
- Building for real users (rural patients, overworked doctors) is very different from building for tech-savvy users
- Simplicity beats complexity in a hackathon—we spent more time removing features than adding them
- Healthcare is hard—we had to be very careful not to over-promise or claim we're replacing doctors

**We're proud of:**
- Building a working end-to-end system in 24 hours
- Focusing on a real problem (not just a cool tech demo)
- Being honest about limitations

---

## How to Run This Project (For Judges/Developers)

If you want to test the demo:

1. Clone the repository:
   ```bash
   git clone https://github.com/Divesh-Kshirsagar/Error_404_3.12_SDG_3.git
   cd Error_404_3.12_SDG_3
   ```

2. Install dependencies and start the backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   python app.py
   ```

3. Start the patient kiosk interface:
   ```bash
   cd patient-app
   npm install
   npm run dev
   ```

4. Start the doctor dashboard:
   ```bash
   cd doctor-app
   npm install
   npm run dev
   ```

5. Open both interfaces in your browser and test the full flow.

**Note:** If OpenAI API limits are hit during the demo, the system falls back to mock data so the demo keeps working.

---

## License & Acknowledgments

**License:** MIT (free for educational use)

**Thanks to:**
- CIH 3.0 organizers for the opportunity and problem statement
- National Health Mission for inspiring the rural healthcare focus
- Open medical datasets that helped us train the model

---

**Built with care for SDG 3 at Central India Hackathon 3.0**

*For questions: [Your Contact Information]*

