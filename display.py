import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import json

def afficher_classement(team_data_list):
    root = tk.Tk()
    root.title("Classement Ligue 1")
    root.geometry("1800x900")
    
    dark_mode = True
    root.configure(bg="#181818")

    frame_left = tk.Frame(root, bg="#303030")
    frame_left.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

    frame_right = tk.Frame(root, bg="#404040")
    frame_right.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)

    selected_team_label = tk.Label(frame_right, text="Sélectionnez une équipe", font=('Roboto', 16), bg="#404040", fg="white")
    selected_team_label.pack(pady=20)

    results_text = tk.Text(frame_right, height=15, width=80, font=('Roboto', 12), bg="#505050", fg="white", wrap=tk.WORD)
    results_text.pack(pady=20)

    headers = ['Position', 'Logo', 'Nom', 'Joués', 'Victoires', 'Nuls', 'Défaites', 'But Marqués', 'But Pris', 'Différence de Buts', 'Points']
    logos = []
    current_highlighted_row = None
    row_colors = ["#303030", "#505050"]

    def toggle_mode():
        nonlocal dark_mode
        if dark_mode:
            root.configure(bg="#FFFFFF")
            frame_left.configure(bg="#F0F0F0")
            frame_right.configure(bg="#E0E0E0")
            selected_team_label.config(bg="#E0E0E0", fg="black")
            results_text.config(bg="#D9D9D9", fg="black")
            for col in range(len(headers)):
                header_label = frame_left.grid_slaves(row=0, column=col)[0]
                header_label.config(bg="#E0E0E0", fg="black")
            dark_mode = False
        else:
            root.configure(bg="#181818")
            frame_left.configure(bg="#303030")
            frame_right.configure(bg="#404040")
            selected_team_label.config(bg="#404040", fg="white")
            results_text.config(bg="#505050", fg="white")
            for col in range(len(headers)):
                header_label = frame_left.grid_slaves(row=0, column=col)[0]
                header_label.config(bg="#404040", fg="white")
            dark_mode = True

    toggle_button = tk.Button(frame_right, text="Toggle Mode", command=toggle_mode, font=('Roboto', 12))
    toggle_button.pack(pady=10)

    def load_match_results():
        with open("ligue1_match_data.json", "r", encoding="utf-8") as file:
            match_data_list = json.load(file)
        return match_data_list

    def display_results(selected_team_name, match_data_list):
        results_text.delete(1.0, tk.END)
        results = [f"{match['home_team']['name']} ({match['home_score']}) vs {match['away_team']['name']} ({match['away_score']})"
                   for match in match_data_list
                   if match['home_team']['name'] == selected_team_name or match['away_team']['name'] == selected_team_name]
        if results:
            results_text.insert(tk.END, "\n".join(results))
        else:
            results_text.insert(tk.END, "Aucun résultat trouvé.")

    def select_team(idx):
        nonlocal current_highlighted_row
        if current_highlighted_row is not None:
            reset_row_colors(current_highlighted_row)

        selected_team = team_data_list[idx]
        selected_team_name = selected_team['name']
        selected_team_label.config(text=selected_team_name)

        match_data_list = load_match_results()
        display_results(selected_team_name, match_data_list)

        current_highlighted_row = idx
        highlight_row(idx, "#FFFF00", "black", ("Roboto", 10, "bold", "italic"))

    def reset_row_colors(row_idx):
        row_color = row_colors[row_idx % 2]
        for col in range(len(headers)):
            label = frame_left.grid_slaves(row=row_idx + 1, column=col)[0]
            label.config(bg=row_color, fg="white", font=("Roboto", 10, "normal"))

    def highlight_row(row_idx, bg_color, fg_color, font_style):
        for col in range(len(headers)):
            label = frame_left.grid_slaves(row=row_idx + 1, column=col)[0]
            label.config(bg=bg_color, fg=fg_color, font=font_style)

    for col, header in enumerate(headers):
        label = tk.Label(frame_left, text=header, font=('Roboto', 10, 'bold'), bg="#404040", fg="white", width=12, borderwidth=2, relief='ridge')
        label.grid(row=0, column=col, sticky='nsew')

    for idx, team in enumerate(team_data_list, start=1):
        row_color = row_colors[idx % 2]

        label_position = tk.Label(frame_left, text=team['position'], bg=row_color, fg="white", width=12, borderwidth=2, relief='ridge')
        label_position.grid(row=idx, column=0, sticky='nsew')

        response = requests.get(team['logo'])
        img_data = Image.open(BytesIO(response.content)).resize((20, 20))
        img = ImageTk.PhotoImage(img_data)
        logos.append(img)
        label_logo = tk.Label(frame_left, image=img, bg=row_color, width=12, borderwidth=2, relief='ridge')
        label_logo.grid(row=idx, column=1, sticky='nsew')

        label_name = tk.Label(frame_left, text=team['name'], bg=row_color, fg="white", width=12, borderwidth=2, relief='ridge')
        label_name.grid(row=idx, column=2, sticky='nsew')

        label_played = tk.Label(frame_left, text=team['matches_played'], bg=row_color, fg="white", width=12, borderwidth=2, relief='ridge')
        label_played.grid(row=idx, column=3, sticky='nsew')

        label_victories = tk.Label(frame_left, text=team['victories'], bg=row_color, fg="white", width=12, borderwidth=2, relief='ridge')
        label_victories.grid(row=idx, column=4, sticky='nsew')

        label_draws = tk.Label(frame_left, text=team['draws'], bg=row_color, fg="white", width=12, borderwidth=2, relief='ridge')
        label_draws.grid(row=idx, column=5, sticky='nsew')

        label_losses = tk.Label(frame_left, text=team['losses'], bg=row_color, fg="white", width=12, borderwidth=2, relief='ridge')
        label_losses.grid(row=idx, column=6, sticky='nsew')

        buts_marques, buts_pris = map(int, team['score'].split(':'))
        difference_buts = buts_marques - buts_pris

        label_buts_marques = tk.Label(frame_left, text=buts_marques, bg=row_color, fg="white", width=12, borderwidth=2, relief='ridge')
        label_buts_marques.grid(row=idx, column=7, sticky='nsew')

        label_buts_pris = tk.Label(frame_left, text=buts_pris, bg=row_color, fg="white", width=12, borderwidth=2, relief='ridge')
        label_buts_pris.grid(row=idx, column=8, sticky='nsew')

        label_diff_buts = tk.Label(frame_left, text=difference_buts, bg=row_color, fg="white", width=12, borderwidth=2, relief='ridge')
        label_diff_buts.grid(row=idx, column=9, sticky='nsew')

        label_points = tk.Label(frame_left, text=team['points'], bg=row_color, fg="white", width=12, borderwidth=2, relief='ridge')
        label_points.grid(row=idx, column=10, sticky='nsew')

        label_name.bind("<Button-1>", lambda e, i=idx-1: select_team(i))

    for col in range(len(headers)):
        frame_left.grid_columnconfigure(col, weight=1)

    root.mainloop()
