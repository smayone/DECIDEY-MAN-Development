from bank_api_integration import get_ach_system

def process_ach_transaction(parsed_data, ach_name):
    try:
        ach_system = get_ach_system(ach_name)
        ach_response = ach_system.process_ach_transaction(parsed_data)
        return {'ach_response': ach_response}
    except ValueError as e:
        return {'error': str(e)}
