def remove_widgets(dashboard):
    for widget in dashboard.winfo_children():
        widget.destroy()