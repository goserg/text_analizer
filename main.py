from text_manager import TextManager


tm = TextManager()
for i in range(1, 11):
    tm.add_book(f"texts/pushkin/tom{i}.txt", "Пушкин Александр Сергеевич", f"Пушкин: Том {i}")

tm.generate_name_distribution_plot(colors=["red", "orange", "yellow", "green", "lightblue", "blue", "violet"])
