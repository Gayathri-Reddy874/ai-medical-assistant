# Medical_data.pdf — Sample Knowledge Base

This is a small sample medical reference document meant for testing the
**AI Medical Assistant** RAG pipeline end-to-end (upload → index → ask). It
covers a handful of common conditions, disease categories, and medications
at a general/informational level — it is **not** a clinical or diagnostic
reference.

## Contents

| Section | Topics covered |
|---|---|
| General Medical Information | Hypertension, Diabetes Mellitus (Type 1 & 2) |
| Cardiovascular Diseases | Coronary Artery Disease (CAD), Heart Failure |
| Respiratory Diseases | Asthma, Chronic Obstructive Pulmonary Disease (COPD) |
| Neurological Disorders | Alzheimer's disease, Parkinson's disease |
| Common Medications | Paracetamol (Acetaminophen), Ibuprofen, Insulin |

## How to use it

1. Upload `Medical_data.pdf` via the Streamlit sidebar ("Upload & Index").
2. Wait for the "Document indexed successfully" confirmation.
3. Ask any of the sample questions below in the main chat panel.

## Sample questions

### General conditions
- What is hypertension and why is it called a silent killer?
- What is considered a normal blood pressure reading, and what's the hypertensive threshold?
- What's the difference between Type 1 and Type 2 diabetes?
- What are the symptoms of diabetes?

### Cardiovascular
- What causes coronary artery disease?
- What are the risk factors for CAD?
- What medications are used to treat heart failure?
- What are the symptoms of heart failure?

### Respiratory
- What triggers asthma symptoms?
- What's the difference between asthma and COPD?
- What causes COPD?

### Neurological
- What are the symptoms of Alzheimer's disease?
- What causes Parkinson's disease?
- Is there a cure for Alzheimer's?

### Medications
- What is paracetamol used for, and what's the risk of overdose?
- What are the side effects of long-term ibuprofen use?
- How is insulin administered?

### Edge-case tests (should answer "I don't know")
These are **not covered** in the document, so a correctly working pipeline
should decline to answer rather than hallucinate:
- What is the treatment for cancer?
- What's the recommended dosage of ibuprofen for adults?
- What causes migraines?

If any of these edge-case questions get a confident, specific answer instead
of "I don't know," that's a sign the retrieval step or the prompt's
"answer only from context" rule needs tightening.

## Disclaimer

This document is for informational and testing purposes only. It is not a
substitute for professional medical advice, diagnosis, or treatment.
