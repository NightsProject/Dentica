
# Dentica

Managing patient records, scheduling appointments, tracking treatment histories, and handling billing are everyday challenges for dental clinics — especially when relying on outdated paper-based systems or spreadsheets. These legacy methods often lead to data inconsistencies, inefficiencies, and security vulnerabilities.

To solve these issues, we present the Dentica Management System — a modern, streamlined solution designed to centralize and simplify clinic operations. Dentica offers a secure, efficient, and user-friendly platform to help dental clinics deliver better service while optimizing their internal workflows.


## Features

- Patient Management: CRUDL operations for patient data management.
- Appointment Scheduling: Automated booking, rescheduling, and cancellation features.
- Treatment History Management: Comprehensive tracking of treatment details linked to appointments.
- Billing & Payment Management: Automated bill generation, payment processing, and financial record keeping.
- Reports & Analytics: Real-time reporting capabilities to drive insights into clinic operations.
- User Authentication: Role-based access control (with the dentist as the primary user and receptionist as a secondary user) to ensure secure system access.



## Authors

- [@NightsProject](https://www.github.com/NightsProject)
- [@Orginary33](https://www.github.com/Ordinary33)
- [@CodeDotCom2](https://github.com/CodeDotcom2)


## _____________________

# Developer Onboarding Guide

Welcome! This project uses **Dev Containers** to provide a consistent development environment. Follow the steps below to get started.

---

## 1. Requirements

Please ensure the following tools are installed on your machine:

| Tool            | Notes                                               | Install Link                                  |
|------------------|------------------------------------------------------|------------------------------------------------|
| [Docker](https://docs.docker.com/get-docker/) | Required to run containers                    | macOS, Windows, or Linux |
| [Visual Studio Code](https://code.visualstudio.com/) | Preferred code editor with container support | — |
| [Dev Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) | VS Code extension to use Dev Containers | — |
| (Optional) [Docker Extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker) | For managing containers visually | — |

---

## 2. Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/NightsProject/Dentica.git
cd Dentica
code .
```

---

## 3. Open in Dev Container

Once the project opens in VS Code:

1. VS Code will detect the `.devcontainer` folder.
2. You will be prompted:  
   > **"Reopen in Container?"**
3. Click **Reopen in Container**.
4. The container will build and initialize. This may take a few minutes on first setup.

---

## 4. Develop and Run the Project

You are now working **inside the container**:

- All tools, interpreters, and services (e.g., Python, MySQL) are pre-installed.
- The environment is isolated and mirrors what others will use.
- Use the VS Code **Terminal**, **Source Control**, and **Debug** panels as usual.

---

## 5. Saving & Sharing Changes

When you're ready to push changes:

```bash
git add .
git commit -m "Your commit message"
git push origin main
```

Or use the **Source Control panel** in VS Code.

---

## 6. Troubleshooting Tips

- If the container fails to build, try:  
  `Dev Containers: Rebuild Container` from the Command Palette (`Ctrl+Shift+P`)
- Ensure Docker is **running** before starting VS Code.
- On macOS/Linux, Docker may require **sudo** access the first time.
