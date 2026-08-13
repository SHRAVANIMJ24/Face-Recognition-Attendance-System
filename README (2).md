<div align="center">

# 🩺 Swasthya Rashmi — Ray of Health

**A full-stack NGO healthcare management platform for blood donation, vaccination, and medicine-donation drives.**

[![Java](https://img.shields.io/badge/Java-JSP%20%2F%20Servlets-ED8B00?style=flat-square&logo=openjdk&logoColor=white)](#)
[![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?style=flat-square&logo=mysql&logoColor=white)](#)
[![Apache Tomcat](https://img.shields.io/badge/Apache%20Tomcat-10.1-F8DC75?style=flat-square&logo=apachetomcat&logoColor=black)](#)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-Frontend-7952B3?style=flat-square&logo=bootstrap&logoColor=white)](#)
[![Status](https://img.shields.io/badge/status-academic%20mini--project-blue?style=flat-square)](#)

[Overview](#-overview) • [Features](#-features) • [Tech Stack](#-tech-stack) • [Screenshots](#-screenshots) • [Getting Started](#-getting-started) • [Database](#-database-schema)

</div>

---

## 📖 Overview

**Swasthya Rashmi ("Ray of Health")** is a Java web application built for a fictional healthcare NGO. Communities often lack one place to coordinate blood camps, vaccination drives, medicine donations, and volunteers — information ends up scattered and hard to act on. This project centralizes all of it behind a single, responsive website:

- Visitors can register for blood-donation and vaccination camps, donate leftover medicine, contribute funds, and sign up to volunteer.
- An admin dashboard gives NGO staff a live view of every registration and donation, backed by a MySQL database.

It was built as a **Mini Project (ITM 501)** for the Bachelor of Engineering in Information Technology program at **Xavier Institute of Engineering, Mumbai (University of Mumbai)**, AY 2024–25.

## ✨ Features

- **Volunteer registration** — sign up for NGO initiatives and campaigns.
- **Blood donation camps** — camp listings, donor eligibility form, and health-history intake (weight, BP, Hb, prior donations, etc.).
- **Vaccination drives** — camp info, an interactive event calendar, and a registration form with medical/insurance details.
- **Medicine donation** — donate leftover medicine or search/request available medicine.
- **Monetary donations** — a donation/payment flow for financial contributions.
- **Testimonials** — success stories from donors, volunteers, and beneficiaries.
- **Admin dashboard** — secure admin login with live record counts and full data tables for every module (volunteers, blood donation, medicine, donations, vaccination).
- **Responsive UI** — mobile-friendly Bootstrap layout with an interactive event calendar and image lightbox.

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, JavaScript, Bootstrap, jQuery |
| Backend | JSP (Jakarta Servlet 6.0), embedded scriptlet logic |
| Database | MySQL, accessed via JDBC (`mysql-connector-j`) |
| Server | Apache Tomcat 10.1+ |
| Tooling | Visual Studio Code |

## 🗺 Site Architecture

<p align="center">
  <img src="screenshots/06-site-architecture.png" alt="Site architecture / page flow diagram" width="850">
</p>

The site is split into a **user side** (Home, Volunteer, Blood Donation, Medicine Donations, Testimonials, Vaccination, Donations) and an **admin side** (login-gated dashboard with per-module record counts and detail views).

## 📸 Screenshots

<table>
<tr>
<td width="50%"><img src="screenshots/01-homepage.png" alt="Homepage"><p align="center"><em>Homepage</em></p></td>
<td width="50%"><img src="screenshots/02-blood-donation.png" alt="Blood donation page"><p align="center"><em>Blood Donation</em></p></td>
</tr>
<tr>
<td width="50%"><img src="screenshots/03-vaccination.png" alt="Vaccination page"><p align="center"><em>Vaccination</em></p></td>
<td width="50%"><img src="screenshots/04-testimonials.png" alt="Testimonials page"><p align="center"><em>Testimonials</em></p></td>
</tr>
<tr>
<td colspan="2"><img src="screenshots/05-admin-dashboard.png" alt="Admin dashboard"><p align="center"><em>Admin Dashboard — live record counts per module</em></p></td>
</tr>
</table>

## 📁 Project Structure

```
Swasthya-Rashmi/
├── index.html                       # Homepage
├── About-Us.html
├── Volunteer.html / Volunteer-form.html / Volunteer-Submit.jsp
├── Blood-Donation.html / Blood-donation-form.jsp / Blood-donation-Submit.jsp
├── Medicine.html / Medicine-form.html / Medicine-Submit.jsp
├── Vaccination.html / Vaccine-Registration-Form.html / Vaccine-Registration-Submit.jsp
├── Donation.html / payment.html / payment-Submit.jsp
├── Testimonials.html
├── Login.jsp                        # Admin authentication
├── Admin-Dashboard.jsp              # Admin dashboard (queries all modules)
├── contact.php
├── style.css
├── css/ , impcss/                   # Stylesheets (Bootstrap + theme overrides)
├── js/ , impjs/                     # Bootstrap, jQuery, custom scripts
├── images/ , impimages/ , fonts/    # Static assets
└── WEB-INF/
    ├── web.xml                      # Servlet 6.0 / Jakarta EE deployment descriptor
    └── classes/
```

> `database/schema.sql` in this repo (added alongside this README) creates the MySQL tables the JSP pages query: `users`, `volunteerapplication`, `blooddonation`, `medicinesdonation`, `vaccineregistration`, `paymentdetails`.

## 🚀 Getting Started

### Prerequisites

- **JDK 17+**
- **Apache Tomcat 10.1+** (the app's `web.xml` targets the Jakarta EE 10 / Servlet 6.0 schema, so it needs Tomcat 10.1 or newer — Tomcat 9 and earlier use the older `javax.servlet` namespace and won't work)
- **MySQL 8+**
- [`mysql-connector-j`](https://dev.mysql.com/downloads/connector/j/) JDBC driver JAR (not bundled — drop it into `WEB-INF/lib/`)

### Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/<your-username>/Swasthya-Rashmi.git
   ```

2. **Create the database**
   ```bash
   mysql -u root -p < database/schema.sql
   ```

3. **Add the MySQL driver** — download `mysql-connector-j-<version>.jar` and place it in `WEB-INF/lib/` (create the folder if it doesn't exist).

4. **Set your DB credentials** — each JSP data page (`Login.jsp`, `Volunteer-Submit.jsp`, `Blood-donation-Submit.jsp`, `Medicine-Submit.jsp`, `Vaccine-Registration-Submit.jsp`, `payment-Submit.jsp`, `Admin-Dashboard.jsp`) currently connects with:
   ```java
   String dbURL = "jdbc:mysql://localhost:3306/swasthya-rashmi";
   String dbUser = "root";
   String dbPassword = "";
   ```
   Update `dbUser` / `dbPassword` in each file to match your local MySQL setup.

5. **Deploy to Tomcat** — copy the `Swasthya-Rashmi/` folder into Tomcat's `webapps/` directory (or package it as a `.war`), then start Tomcat.

6. **Open the site**
   ```
   http://localhost:8080/Swasthya-Rashmi/index.html
   ```
   Log in to the admin dashboard at `Login.jsp` with the seed account from `schema.sql` (`admin` / `admin123`) — **change this before deploying anywhere public.**

## 🗄 Database Schema

| Table | Purpose |
|---|---|
| `users` | Admin login credentials |
| `volunteerapplication` | Volunteer sign-ups |
| `blooddonation` | Blood donation camp registrations + donor health history |
| `medicinesdonation` | Leftover medicine donations |
| `vaccineregistration` | Vaccination camp registrations + medical/insurance details |
| `paymentdetails` | Monetary donation/payment records |

Full column definitions are in [`database/schema.sql`](database/schema.sql).

## 🔭 Future Enhancements

- Real-time notifications for upcoming camps and drives
- Geolocation-based search for nearby blood/vaccination centers
- Dedicated mobile app
- Integrated payment gateway (current flow captures card details but doesn't process real payments)
- AI chatbot for user assistance
- Analytics dashboard for donation/engagement metrics
- Externalize DB credentials (e.g. to a config file or environment variables) instead of hardcoding them per-page

## 🙏 Acknowledgments

- UI built on top of a Bootstrap-based charity/NGO HTML template, customized for this project's pages, forms, and content.
- Icons and stock imagery from the template's free asset pack.

## 📄 License

This project was created for academic purposes as part of a university mini-project. The front-end is customized from a third-party HTML/CSS template — please check that template's license before reusing the design commercially. The JSP/backend code and database schema are original to this project.
