class ContinueOnError(Exception):
    pass

def raise_error(msg):
    try:
        raise ContinueOnError(f"An error occurred: \n{msg}\n\nDo you want to continue? (y/n)")
    except ContinueOnError as e:
        user_input = input(str(e))
        if user_input.lower() == 'y':
            print("Continuing...")
        else:
            print("Error: Operation aborted.")
