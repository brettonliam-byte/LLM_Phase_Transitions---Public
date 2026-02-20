import json
import os

def generate_dashboard():
    config_path = 'dashboard_config.json'
    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found.")
        return

    with open(config_path, 'r') as f:
        config = json.load(f)

    project_name = config.get('project_name', 'LLM Experiments Dashboard')
    experiments = config.get('experiments', [])
    github_user = config.get('github_username', 'brettonliam-byte')
    repo_name = config.get('repository_name', 'LLM_Phase_Transitions')
    base_url = f"https://{github_user}.github.io/{repo_name}/"

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">
    <style>
        body {{ background-color: #f8f9fa; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
        .hero-section {{ background: linear-gradient(135deg, #212529 0%, #343a40 100%); color: white; padding: 60px 0; border-bottom: 5px solid #0d6efd; }}
        .card {{ border: none; transition: transform 0.2s, box-shadow 0.2s; border-radius: 12px; height: 100%; }}
        .card:hover {{ transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }}
        .card-icon {{ font-size: 2.5rem; color: #0d6efd; margin-bottom: 15px; }}
        .btn-view {{ border-radius: 25px; padding: 10px 25px; font-weight: 600; }}
        .footer {{ padding: 40px 0; color: #6c757d; font-size: 0.9rem; }}
        .qr-placeholder {{ max-width: 150px; margin: 20px auto; border: 1px solid #dee2e6; padding: 10px; background: white; border-radius: 8px; }}
    </style>
</head>
<body>

<header class="hero-section text-center">
    <div class="container">
        <h1 class="display-4 fw-bold">{project_name}</h1>
        <p class="lead mb-4">A central hub for visualizing Large Language Model performance and phase transitions.</p>
        <div class="qr-placeholder">
            <img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={base_url}" alt="Scan to view on mobile" class="img-fluid">
            <p class="small text-dark mt-2 mb-0">Scan Me</p>
        </div>
    </div>
</header>

<main class="container my-5">
    <div class="row g-4">
"""

    for exp in experiments:
        title = exp.get('title', 'Untitled Experiment')
        desc = exp.get('description', 'No description provided.')
        path = exp.get('path', '#')
        icon = exp.get('icon', 'bi-file-earmark-bar-graph')
        
        html_template += f"""
        <div class="col-md-6 col-lg-4">
            <div class="card p-4 text-center">
                <div class="card-body d-flex flex-column">
                    <i class="bi {icon} card-icon"></i>
                    <h3 class="card-title h5 fw-bold">{title}</h3>
                    <p class="card-text text-muted flex-grow-1">{desc}</p>
                    <a href="{path}" class="btn btn-outline-primary btn-view mt-3">View Visualization</a>
                </div>
            </div>
        </div>"""

    html_template += f"""
    </div>
</main>

<footer class="footer text-center bg-white border-top">
    <div class="container">
        <p>&copy; 2026 {project_name} | Created by {github_user}</p>
        <p>Source Code available on <a href="https://github.com/{github_user}/{repo_name}" class="text-decoration-none">GitHub</a></p>
    </div>
</footer>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print("Successfully generated index.html dashboard.")

if __name__ == "__main__":
    generate_dashboard()
