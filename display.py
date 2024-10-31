import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

def afficher_classement(team_data_list):
    root = tk.Tk()
    root.title("Classement Ligue 1")
    root.geometry("1800x900")

    frame_left = tk.Frame(root, width=900, height=600)
    frame_left.grid(row=0, column=0, sticky='nsew')
    
    frame_right = tk.Frame(root, width=900, height=600, bg="white")
    frame_right.grid(row=0, column=1, sticky='nsew')
    
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)

    selected_team_label = tk.Label(frame_right, text="Sélectionnez une équipe", font=('Arial', 16), width=20, height=5)
    selected_team_label.pack(pady=20)

    headers = ['Position', 'Logo', 'Nom', 'Joués', 'Victoires', 'Nuls', 'Défaites', 'But Marqués', 'But Pris', 'Différence de Buts', 'Points']
    logos = []
    current_highlighted_row = None
    row_colors = ["#303030", "#505050"]

    def select_team(idx):
        nonlocal current_highlighted_row
        if current_highlighted_row is not None:
            reset_row_colors(current_highlighted_row)

        selected_team = team_data_list[idx]
        selected_team_label.config(text=selected_team['name'])

        current_highlighted_row = idx
        highlight_row(idx, "#FFFF00", "black", ("Roboto", 10, "bold", "italic"))

    def reset_row_colors(row_idx):
        row_color = row_colors[row_idx % 2]
        for col in range(len(headers)):
            label = frame_left.grid_slaves(row=row_idx+1, column=col)[0]
            label.config(bg=row_color, fg="white", font=("Roboto", 10, "normal"))

    def highlight_row(row_idx, bg_color, fg_color, font_style):
        for col in range(len(headers)):
            label = frame_left.grid_slaves(row=row_idx+1, column=col)[0]
            label.config(bg=bg_color, fg=fg_color, font=font_style)

    for col, header in enumerate(headers):
        label = tk.Label(frame_left, text=header, font=('Arial', 10, 'bold'), bg="#404040", fg="white", width=12, borderwidth=2, relief='ridge')
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
