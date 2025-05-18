# **Bio Analyze API** 🚀

<img src="/body_analyzer/static/img/bio_analyze.jpg" alt="Logo" width="300" />

[![Version](https://img.shields.io/badge/version-1.0.0--beta-blue)]()
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)]()
[![License](https://img.shields.io/badge/license-MIT-yellow)]()  
[![Deployed on Heroku](https://img.shields.io/badge/Heroku-Live-purple)](https://your-heroku-app.herokuapp.com)  
> **Biometric analysis API designed for healthcare professional nutritionists and personal trainers.**

---

## **Index**
1. [Description](#description)
2. [Main Features](#main-features)
3. [Requirements](#requirements)
4. [Installation and use](#installation-and-use)
5. [Local tests](#local-tests)
6. [Available endpoints](#available-endpoints)
7. [Flowchart](#flowchart)
8. [Production](#production)
9. [Endnotes](#endnotes)
10. [Contributions](#contributions)
11. [License](#license)


---

## **Description**

The **Bio Analyze** API allows for advanced biometric calculations and initial nutritional recommendations from basic user data. 

It is designed as a **BACKEND** tool that can be integrated with a web form or app to capture input data.

It is ideal for:
- **Personal trainers**: Initial setup of training plans and goals.
- **Nutritionists**: Personalised dietary recommendations.
- **Health professionals**: Fast and accurate assessments.

You can try the **beta** version in production here: 🌐 [**Body Analyzer API in Heroku**](https://bioanalyze-f0d59edaef22.herokuapp.com)

---

## **Main Features**

1. **Advanced calculations:**

- **BMI**: Detects if high BMI is due to muscle mass or excess fat.
- **Body fat percentage**: Estimates based on proven formulas.
- **BMR and daily calories**: Adjusted according to the goal.

2. **Customizable goals:**
- Lose fat.
- Maintain weight.
- Gain muscle mass.

3. **Macronutrient recommendations**: Protein, carbohydrate and fat ratios according to the goal.

4. **Easy integration**: Designed to be integrated into a website or application.
---

## **Requirements**

- **Python 3.13+**
- Required libraries (installed automatically from `pyproject.toml` file).
---

## **Installation and use**

### **1. Clone the repository**
```bash
git clone https://github.com/your_user/body_analyzer.git
cd body_analyzer
```
### **2. Install the dependencies**
```bash
pip install .
```
Or, if you prefer to use the Makefile:
```bash
make install
```
### **3. Run the API locally**
```bash
python src/body_analyzer/main.py
```
The API will be available at http://127.0.0.1:5000

---

## **Local tests**

You can test the API locally with Postman, cURL, or any tool that supports HTTP requests.
Here is an example of the main endpoint:

Example of requests with cURL
```bash
curl -X POST http://127.0.0.1:5000/informe_completo \
-H "Content-Type: application/json" \
-d '{
  "peso": 90,
  "altura": 165,
  "edad": 44,
  "genero": "h",
  "cuello": 41,
  "cintura": 99,
  "cadera": 105,
  "objetivo": "perder grasa"
}'
```

### Expected response

```bash
{
  "interpretaciones": {
    "ffmi": "Muy cerca del máximo potencial.",
    "imc": "El IMC es alto, pero puede estar influenciado por una alta masa muscular.",
    "porcentaje_grasa": "Alto",
    "ratio_cintura_altura": "Alto riesgo",
    "rcc": "N/A"
  },
  "resultados": {
    "agua_total": 46.4,
    "calorias_diarias": 1762.69,
    "ffmi": 24.28,
    "imc": 33.06,
    "macronutrientes": {
      "carbohidratos": 176.27,
      "grasas": 39.17,
      "proteinas": 176.27
    },
    "masa_muscular": 66.105,
    "peso_saludable": {
      "max": 67.79,
      "min": 50.37
    },
    "porcentaje_grasa": 26.55,
    "ratio_cintura_altura": 0.6,
    "rcc": "N/A",
    "sobrepeso": 22.21,
    "tmb": 1836.14
  }
}
```

---
## **Available Endpoints**

_Method / Path / Description_

* GET / Verifies that the server is running.

* POST /full_report / Generates a full biometric report.
* POST /calculate_bmi / Calculates the body mass index (BMI).
* POST /calculate_weight_body_fat / Calculates body fat in kilograms.
* POST /daily_calories / Calculates the recommended daily calories.
* POST /macronutrients / Calculates the macronutrient distribution.
* And more in the endpoints.py file
---

## **Flowchart**


[![](https://mermaid.ink/img/pako:eNptkUtOwzAQhq9ied1eIAskRCsEElBRYIG8GewhsYg90dhGgqYHYsGKI-RiOE7UglSv5h9_895JTQZlJWuGrhEPK-VFfo8hAVsSy-VZv_bvwzcIA5GCuN7e3fbifHM1cdkozBO01sxMLyal7fDjJ-yPo-AXxIw6Ui82TBoDOIs-0gT_cxX8Ej0yCMaQ2ggmt_FiyQ1fka0e690fPqYMRz0PEBnrMV6TQz82Qh6D6JAD-dzaJxjIaeahT7e8ZiYupbqEIULRysuFdMgOrMk73I2hSsYGHSpZZdMAvymp_D5zkCJtP7yWVeSEC8mU6kZWr9CGrFKXl4crC_kQ7uDtwD8THTUaG4lvppOVy-1_AZSnoCA?type=png)](https://mermaid.live/edit#pako:eNptkUtOwzAQhq9ied1eIAskRCsEElBRYIG8GewhsYg90dhGgqYHYsGKI-RiOE7UglSv5h9_895JTQZlJWuGrhEPK-VFfo8hAVsSy-VZv_bvwzcIA5GCuN7e3fbifHM1cdkozBO01sxMLyal7fDjJ-yPo-AXxIw6Ui82TBoDOIs-0gT_cxX8Ej0yCMaQ2ggmt_FiyQ1fka0e690fPqYMRz0PEBnrMV6TQz82Qh6D6JAD-dzaJxjIaeahT7e8ZiYupbqEIULRysuFdMgOrMk73I2hSsYGHSpZZdMAvymp_D5zkCJtP7yWVeSEC8mU6kZWr9CGrFKXl4crC_kQ7uDtwD8THTUaG4lvppOVy-1_AZSnoCA)


---

## **Production**

The API is deployed on Heroku in beta: 🌐 Body Analyzer API on Heroku
https://bioanalyze-f0d59edaef22.herokuapp.com

Testing in production,
You can use the same routes and data mentioned in the previous sections
but replace http://127.0.0.1:5000 with the Heroku URL.
---

## **Endnotes**

Future Releases
* Authentication implementation.
* Database integration.
* Creation of a frontend to facilitate the use of the API.
---

## **Contributions**

This project is open for contributions! If you'd like to contribute:

1. Fork the repository.
2. Create a new branch for your changes:
```bash
git checkout -b feature/new-feature
```
3. Commit your changes and make descriptive commits:
```bash
git commit -m "Added new feature to calculate ..."
```
4. Submit a pull request explaining your changes.

Please make sure to follow coding best practices and, if possible, add unit tests for any new features.
---

## **License**

Copyright © 2024 Pablo Techera Sosa. All rights reserved.

---

### 1. Permissions

Permission is granted to anyone to contribute, modify, and/or improve this project under the following conditions:

1. **Personal and Educational Use**:
- You may use this project for educational or learning purposes without any restrictions.

2. **Modifications and Collaborations**:
- You may modify the code and collaborate on the development by submitting pull requests to the official repository.
- Contributions will be reviewed and approved by the project's authors or maintainers.

3. **Redistribution and Derivative Uses**:
- If you decide to redistribute a modified version of the project, you must include this same licence along with the original author's copyright.
- Commercial use of the project or its modifications is not permitted without the explicit written permission of the author.

---

### 2. Restrictions

1. **Copyright**:
- This project remains the intellectual property of Pablo Techera Sosa.
- All accepted contributions to the official repository are considered licensed for use within the original project under the terms of this license.

2. **Commercial Use**:
- Commercial use of the project, whether in its original or modified form, is prohibited without express written permission.

3. **Limitation of Liability**:
- This software is provided "as is", without a warranty of any kind, express or implied. 
- In no event shall the authors be liable for damages or problems arising from the use of the project.

---

### 3. How to Contribute

If you wish to contribute to this project:

1. Fork the repository.
2. Create a new branch for your modifications.
3. Send a pull request clearly describing the changes made.

---

### 4. Final Note

By contributing to this project, you agree that your contributions may be used and distributed under the terms of this licence.
