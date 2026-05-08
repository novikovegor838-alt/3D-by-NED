from datetime import date, timedelta
import time
import flet as ft
import json

COLOR_MAP = {
    "🔴 Красный": "#cc0000",
    "🔵 Синий": "#000077",
    "🟡 Жёлтый": "#d3ac00",
    "🟠 Оранжевый": "#bb7800",
    "⚪ Белый": "#ffffff",
    "⚫ Чёрный": "#000000",
    "🟢 Зелёный": "#008c00",
    "⚪⚫ Серый": "#888888",
    "🟣 Фиолетовый": "#530085",
    "🟤 Коричневый": "#592e00"
}

def main(page: ft.Page):
    page.title = "3D by NED"
    page.window.width = 461
    page.window.height = 800
    page.padding = 0
    page.theme_mode = ft.ThemeMode.DARK

    """ Верхний фрейм """
    top_frame = ft.Container(content=ft.Row([
        ft.Text("3D by NED", size=28, weight="bold", expand=True, color="#cccc88", italic=True),
        ft.IconButton(icon=ft.Image(src="icons/3D by NED icon.png", width=50, height=50), on_click=lambda e: settings())
    ],
    alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
    padding=ft.padding.only(left=15, right=15, top=15, bottom=15),
    bgcolor="#490021"
    )

    # колонка для виджетов, которые сейчас на экране
    content_area = ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS)

    """ Кнопки навигации """
    bottom_frame = ft.Container(content=ft.Row([
        ft.IconButton(icon=ft.Image(src="icons/иконки принтера для 3D by NED.png",
                                    width=35, height=35), on_click=lambda e: home()),

        ft.IconButton(icon=ft.Image(src="icons/иконка статистики для 3D by NED.png",
                                    width=35, height=35), on_click=lambda e: statistics()),

        ft.IconButton(icon=ft.Image(src="icons/иконка склада для 3D by NED.png",
                                    width=35, height=35), on_click=lambda e: warehouse()),

        ft.IconButton(icon=ft.Image(src="icons/иконка мастерской для 3D by NED.png",
                                    width=35, height=35), on_click=lambda e: workshop())
    ], height=50,
    alignment=ft.MainAxisAlignment.SPACE_AROUND),
    padding=ft.padding.only(left=10, right=10, top=10, bottom=10),
    bgcolor="#490021"
    )

    """ Функция главной страницы """
    def home():
        content_area.controls.clear()

        buttons = ft.Container(ft.Row([ft.ElevatedButton("+ Новый заказ",  width=180, height=90, style=ft.ButtonStyle(
            bgcolor="#0056bd", color="#ccffff", shape=ft.RoundedRectangleBorder(radius=6)), on_click=lambda e: new_order()),
                          ft.ElevatedButton("Архив заказов",  width=180, height=90, style=ft.ButtonStyle(
            bgcolor="#51007e", color="#ccffff", shape=ft.RoundedRectangleBorder(radius=6)), on_click=lambda e: archive_orders())],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=20), padding=ft.padding.only(left=20, right=20, top=20, bottom=10))

    # карточки заказов
        orders_cards = ft.ListView([],
        spacing=2,
        expand=True)

        with open("orders.json", "r", encoding="utf-8") as o:
            orders = json.load(o)

        for i, order in enumerate(orders):
            created_date = date.fromisoformat(order["created_date"])
            deadline = created_date + timedelta(days=order["complete"])
            remaining = (deadline - date.today()).days

            order_card = ft.Card(
                    ft.Container(
                        ft.Row([
                            ft.Column([
                                ft.Text(order["name"], size=20, weight="bold", color="#008d95"),
                                ft.Text(f"Срок: {remaining}", size=16, color="#716700"),
                                ft.Text(f"Стоимость: {order["price"]}", size=18, color="#005f05")
                            ], spacing=5),
                            ft.ElevatedButton("Готов!", bgcolor="#c69c00", width=100, height=50,
                                              on_click=lambda e, oid=order["id"]: complete_order(oid)
                                              )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ), padding=ft.padding.only(left=15, right=15)
                    ), height=100
                )

            orders_cards.controls.append(order_card)

        content_area.controls.extend([buttons, orders_cards])
        page.update()

    """ Функция меню статистики """
    def statistics():
        with open("statistics.json", "r", encoding="utf-8") as s:
            statistics = json.load(s)

        content_area.controls.clear()

        statistic_labels = ft.Container(
            ft.Row([ft.Column([
                ft.Text("Статистика", size=26, color="#c0001e", weight="bold", italic=True),
                ft.Text(f"Всего выполнено заказов: {statistics["orders"]}", size=18, color="#0084be"),
                ft.Text(f"Всего заработано: {statistics["cash"]} руб.", size=18, color="#00bc63"),
                ft.Text(f"Средний заработок: {statistics["average_cash"]} руб.", size=18, color="#c27f00"),
                ft.Text(f"Потрачено катушек: {statistics["spent_filaments"]}", size=18, color="#c27f00")
            ], spacing=40, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            ], alignment=ft.MainAxisAlignment.CENTER),
            padding=ft.padding.only(top=80)
        )

        content_area.controls.extend([statistic_labels])
        page.update()

    """ Функция склада """
    def warehouse():
        content_area.controls.clear()

        filament_grid = ft.GridView(
            expand=True,
            runs_count=2,
            max_extent=200,
            child_aspect_ratio=1.0,
            spacing=10, run_spacing=10
        )

        with open("warehouse_objects.json", "r", encoding="utf-8") as w:
            objects = json.load(w)

        for i, object in enumerate(objects):
            filament_cards = ft.Card(
                ft.Container(ft.Column([
                    ft.Text(object["tipe"], size=26, weight="bold", color="#00fe95"),
                    ft.Text(f"{object["weight"]} гр", size=20, color="#0093c3", weight="bold"),
                    ft.ElevatedButton("Списать", color="#77ffff",
                                      style=ft.ButtonStyle(side=ft.BorderSide(width=3, color="#aabbdd")), bgcolor="#00000000",
                                      on_click=lambda e, oid=object["id"]: delete_object(oid))
                ], alignment=ft.MainAxisAlignment.CENTER),
                    alignment=ft.Alignment.CENTER, bgcolor=object["color_object"], expand=True, padding=20, border_radius=10)
            )

            filament_grid.controls.append(filament_cards)

        container_grid = ft.Container(filament_grid, expand=True, padding=20)

        content_area.controls.append(container_grid)
        page.update()

    """ Функция мастерской """
    def workshop():
        with open("notes.txt", "r", encoding="utf-8") as n:
            notes = n.read()

        content_area.controls.clear()

        filament_consumtion = ft.TextField(label="Расход пластика", border_radius=15, width=180, height=40, bgcolor="#805000",
                                    color="black", border_color="#770000", border_width=3)
        time_print = ft.TextField(label="Время печати", border_radius=15, width=180, height=40, bgcolor="#805000",
                                    color="black", border_color="#770000", border_width=3)
        result = ft.Text("Результат", color="#c69c00")

        button_new_object = ft.Container(ft.Row([
            ft.ElevatedButton("+ Новая катушка пластика на склад", bgcolor="#c69c00", width=170, height=80,
                              style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15)),
                              on_click=lambda e: new_object(), color="#653e00"),
            ft.Column([filament_consumtion,
                       time_print,
                       ft.Container(ft.Row([result], alignment=ft.MainAxisAlignment.CENTER
                                           ), width=180, height=30, bgcolor="#560700",
                                    border_radius=12),
                       ft.ElevatedButton("Посчитать", bgcolor="#a30031", width=140, height=40, on_click=lambda e: calculate())],
                      horizontal_alignment=ft.MainAxisAlignment.CENTER, spacing=10)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=20), padding=ft.padding.only(top=20, left=30, right=30))

        textbox = ft.TextField(hint_text="3D-печатные заметки...", bgcolor="#805000", color="black", border_color="#770000",
                         border_width=3, multiline=True, filled=True, width=400, height=300, min_lines=12, max_lines=12,
                               value=notes, border_radius=20
                               )

        notes = ft.Container(ft.Column([textbox,
            ft.ElevatedButton("Сохранить", bgcolor="#a30031", width=200, height=40, on_click=lambda e: notes())
        ], spacing=10, horizontal_alignment=ft.MainAxisAlignment.CENTER),
            padding=ft.padding.only(top=30, left=30, right=30, bottom=20))

        content_area.controls.extend([button_new_object, notes])
        page.update()

        def notes():
            with open("notes.txt", "w", encoding="utf-8") as n:
                n.write(textbox.value)

        def calculate():
            try:
                with open("settings.json", "r", encoding="utf-8") as set:
                    settings = json.load(set)

                resultat = int(filament_consumtion.value) * settings["price_of_gr_filament"] + int(time_print.value) * settings["price_of_hour"]

                result.value = str(resultat * settings["margin"])
                page.update()
            except Exception:
                result.value = "Где числа?"
                page.update()


    """ Функции кнопок """
# Функция добавления нового заказа
    def new_order():
        name_order = ft.TextField(label="Название")
        complete_order = ft.TextField(label="Срок выполнения")
        price_order = ft.TextField(label="Стоимость")

        dialog = ft.AlertDialog(
            title=ft.Text("Новый заказ!", color="#a90060", weight="bold"),
            content=ft.Column([
                name_order,
                complete_order,
                price_order
            ], height=350), actions=[ft.ElevatedButton("Отмена", bgcolor="#c69c00", width=120, height=40,
                                                       on_click=lambda e: close_dialog()),
                                     ft.ElevatedButton("Сохранить", bgcolor="#a30031", width=120, height=40,
                                                       on_click=lambda e: save_order())],
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            modal=True, on_dismiss=True,
        )

        page.show_dialog(dialog)
        dialog.open = True
        page.update()

        def close_dialog():
            dialog.open = False
            page.update()

        def save_order():
            try:
                with open("orders.json", "r", encoding="utf-8") as o:
                    orders = json.load(o)

                new_order = {
                    "id": time.time(), "name": name_order.value, "created_date": date.today().isoformat(),
                    "complete": int(complete_order.value), "price": int(price_order.value)
                }
                orders.append(new_order)

                with open("orders.json", "w", encoding="utf-8") as o:
                    json.dump(orders, o, indent=2, ensure_ascii=False)
                    #o.flush()

                print("SAVE!")
                close_dialog()
            # Пересоздаём главную страницу, а не просто обновляем интерфейс
                home()
            except Exception:
                name_order.value = "ВВЕДИ ДАННЫЕ!"

# Архив заказов
    def archive_orders():
        with open("archive_orders.json", "r", encoding="utf-8") as a:
            archive = json.load(a)

        archive_cards = ft.ListView([], spacing=2, expand=True)

        for j, arch in enumerate(archive):
            archive_card = ft.Card(
                ft.Container(
                    ft.Row([
                        ft.Column([
                            ft.Text(arch["name"], size=14, color="#cba200", weight="bold"),
                            ft.Text(f"Заработок: {arch["price"]} руб.", size=12, color="#009d33")
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Text(f"id: {arch["id"]}", color="#8a008e", size=10, weight="bold")
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), padding=ft.padding.only(left=7, right=7)
                ), height=100
            )

            archive_cards.controls.append(archive_card)

        dialog = ft.AlertDialog(
            title=ft.Text("Архив!", color="#a90060", weight="bold"),
            content=ft.Container(archive_cards, width=430, height=500),
            actions=[ft.ElevatedButton("Назад", bgcolor="#a30031", width=120, height=40, on_click=lambda e: close_dialog())],
            actions_alignment=ft.MainAxisAlignment.END,
            modal=True, on_dismiss=True,
        )

        def close_dialog():
            dialog.open = False
            page.update()

        page.show_dialog(dialog)
        dialog.open = True
        page.update()

# Добавления нового филамента на склад
    def new_object():
        tipe = ft.TextField(label="Тип")
        weight = ft.TextField(label="Вес")
        list_color = ft.Dropdown(
                    label="Цвет филамента", border_radius=12, border_color="#940100", color="#b88e00",
                    options=[
                        ft.dropdown.Option(text="🔴 Красный"),
                        ft.dropdown.Option(text="🟠 Оранжевый"),
                        ft.dropdown.Option(text="🟡 Жёлтый"),
                        ft.dropdown.Option(text="🟢 Зелёный"),
                        ft.dropdown.Option(text="🔵 Синий"),
                        ft.dropdown.Option(text="🟣 Фиолетовый"),
                        ft.dropdown.Option(text="🟤 Коричневый"),
                        ft.dropdown.Option(text="⚫ Чёрный"),
                        ft.dropdown.Option(text="⚪ Белый"),
                        ft.dropdown.Option(text="⚪⚫ Серый")
                    ]
                )

        dialog = ft.AlertDialog(
            title=ft.Text("Новый филамент!", color="#a90060", weight="bold"),
            content=ft.Column([
                tipe,
                weight,
                list_color
            ], height=350), actions=[ft.ElevatedButton("Отмена", bgcolor="#c69c00", width=120, height=40,
                                                       on_click=lambda e: close_dialog()),
                                     ft.ElevatedButton("Добавить", bgcolor="#a30031", width=120, height=40,
                                                       on_click=lambda e: save_object())],
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            modal=True, on_dismiss=True
        )

        def close_dialog():
            dialog.open = False
            page.update()

        def save_object():
            try:
                with open("warehouse_objects.json", "r", encoding="utf-8") as w:
                    objects = json.load(w)

                color_obj = list_color.value
                color = COLOR_MAP.get(color_obj)

                new_object = {"tipe": tipe.value, "weight": int(weight.value), "color_object": color, "id": time.time()}
                objects.append(new_object)

                with open("warehouse_objects.json", "w", encoding="utf-8") as w:
                    json.dump(objects, w, indent=2, ensure_ascii=False)

                print("SAVE!")
                close_dialog()
                #page.update()
                workshop()
            except Exception:
                tipe.value = "ВВЕДИ ДАННЫЕ!"

        page.show_dialog(dialog)
        dialog.open = True
        page.update()


# ЗАВЕРШЕНИЕ ЗАКАЗА И ДОБАВЛЕНИЕ В АРХИВ!
    def complete_order(order_id):
        # Открытие нужных файлов
        # Заказы
        with open("orders.json", "r", encoding="utf-8") as o:
            orders = json.load(o)

        # Статистика
        with open("statistics.json", "r", encoding="utf-8") as s:
            statistics = json.load(s)

        # Архив заказов
        with open("archive_orders.json", "r", encoding="utf-8") as a:
            archive = json.load(a)

        completed_order = None
        for i, order in enumerate(orders):
            if order["id"] == order_id:
                completed_order = orders.pop(i)

                statistics["orders"] += 1
                statistics["cash"] += order["price"]

                break

        if completed_order:
            with open("orders.json", "w", encoding="utf-8") as o:
                json.dump(orders, o, ensure_ascii=False, indent=2)

            archive.append(completed_order)
            with open("archive_orders.json", "w", encoding="utf-8") as a:
                json.dump(archive, a, ensure_ascii=False, indent=2)

    # МАТЕМАТИКА СТАТИСТИКИ
            average_cash = statistics["cash"] / statistics["orders"]

            statistics["average_cash"] = average_cash

        # Запись данных
            with open("statistics.json", "w", encoding="utf-8") as s:
                json.dump(statistics, s, indent=2, ensure_ascii=False)

            home()

    def settings():
        with open("settings.json", "r", encoding="utf-8") as set:
            settings = json.load(set)

        price_of_hour = ft.TextField(label="Цена за час печати", value=settings["price_of_hour"])
        price_of_gr_filament = ft.TextField(label="Цена за грамм филамента", value=settings["price_of_gr_filament"])
        margin = ft.TextField(label="Навар", value=settings["margin"])

        settings_dialog = ft.AlertDialog(
            title=ft.Text("Настройки", color="#a90060", weight="bold"),
            content=ft.Column([
                price_of_hour,
                price_of_gr_filament,
                margin,
                ft.Text("App created by NED", size=12, color="#666666")
            ], height=300, spacing=20, horizontal_alignment=ft.MainAxisAlignment.CENTER),
            actions=[ft.ElevatedButton("Закрыть", bgcolor="#c69c00", width=120, height=40,
                                                       on_click=lambda e: close_settings_dialog()),
                        ft.ElevatedButton("Применить", bgcolor="#a30031", width=130, height=40,
                                                       on_click=lambda e: apply())],
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        def close_settings_dialog():
            settings_dialog.open = False
            page.update()

        def apply():
            try:
                settings["price_of_hour"] = int(price_of_hour.value)
                settings["price_of_gr_filament"] = int(price_of_gr_filament.value)
                settings["margin"] = int(margin.value)

                with open("settings.json", "w", encoding="utf-8") as set:
                    json.dump(settings, set, ensure_ascii=False)

                close_settings_dialog()
            except Exception:
                price_of_hour.value = "ВВЕДИ ДАННЫЕ"

        page.show_dialog(settings_dialog)
        settings_dialog.open = True
        page.update()

    def delete_object(object_id):
        with open("warehouse_objects.json", "r", encoding="utf-8") as w:
            objects = json.load(w)

        with open("statistics.json", "r", encoding="utf-8") as s:
            statistic = json.load(s)

        for j, object in enumerate(objects):
            if object["id"] == object_id:
                objects.pop(j)

                with open("warehouse_objects.json", "w", encoding="utf-8") as w:
                    json.dump(objects, w, indent=2, ensure_ascii=False)

                statistic["spent_filaments"] += 1

                with open("statistics.json", "w", encoding="utf-8") as s:
                    json.dump(statistic, s, ensure_ascii=False)
                break
        warehouse()

# сборка всех элементов в одну колонку
    main_layout = ft.Column(controls=[top_frame, content_area, bottom_frame],
                            spacing=0, expand=True)

# Показ главного лейаута и домашней страницы
    page.add(main_layout)
    home()

ft.app(target=main)