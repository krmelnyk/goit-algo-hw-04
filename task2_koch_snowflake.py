import turtle


def koch_curve(turtle_obj: turtle.Turtle, order: int, size: float) -> None:
    """Draw a Koch curve segment for the given recursion order."""
    if order == 0:
        turtle_obj.forward(size)
    else:
        # Split the segment into four smaller Koch segments.
        size /= 3.0
        koch_curve(turtle_obj, order - 1, size)
        turtle_obj.left(60)
        koch_curve(turtle_obj, order - 1, size)
        turtle_obj.right(120)
        koch_curve(turtle_obj, order - 1, size)
        turtle_obj.left(60)
        koch_curve(turtle_obj, order - 1, size)


def draw_snowflake(order: int, size: float = 300) -> None:
    """Draw a Koch snowflake using three Koch curve segments."""
    screen = turtle.Screen()
    turtle_obj = turtle.Turtle()
    turtle_obj.speed(0)

    # A Koch snowflake consists of three Koch curve sides.
    for _ in range(3):
        koch_curve(turtle_obj, order, size)
        turtle_obj.right(120)

    screen.mainloop()


def get_recursion_level() -> int:
    """Ask the user for a non-negative recursion level."""
    while True:
        user_input = input(
            "Enter the level of the Koch snowflake (0 or higher): "
        )

        try:
            level = int(user_input)
        except ValueError:
            # Keep asking until the input can be parsed as an integer.
            print("Please enter an integer.")
            continue

        if level >= 0:
            return level

        print("Please enter a non-negative integer.")


if __name__ == "__main__":
    level = get_recursion_level()
    draw_snowflake(level)
