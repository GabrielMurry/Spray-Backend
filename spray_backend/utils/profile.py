from .common_imports import *
from .common_functions import *
import pytz
# Define the PST timezone
pst_timezone = pytz.timezone('America/Los_Angeles')  # 'America/Los_Angeles' corresponds to Pacific Standard Time (PST)

def create_session_data(title, date, data):
    return {
        'title': title,
        'date': date,
        'data': data,
    }

def get_session_boulders(sent_boulders, user_id):
    session = 1
    sessions = []
    session_boulders = []
    boulders = []
    for index, sent_boulder in enumerate(sent_boulders):
        session_boulders.append(get_boulder_data(sent_boulder.boulder, user_id, sent_boulder))
        # if we reach end of boulders array or current send date != next boulder's send date, append session to boulders
        formatted_send_date = sent_boulder.date_created.astimezone(pst_timezone).strftime('%B %d, %Y')
        if index == len(sent_boulders) - 1 or formatted_send_date != sent_boulders[index + 1].date_created.astimezone(pst_timezone).strftime('%B %d, %Y'):
            boulders.append(create_session_data(session, formatted_send_date, session_boulders))
            sessions.append(session)
            session += 1
            session_boulders = []
    sessions.reverse()
    for index, boulder in enumerate(boulders):
        boulder['title'] = sessions[index]
    return boulders

def get_sent_boulders(user_id, spraywall_id):
    return (
        Send.objects
        .filter(person__id=user_id, boulder__spraywall__id=spraywall_id)
        .select_related('boulder')
        .order_by('-date_created') # most oldest to most recent send
        .prefetch_related('boulder__send_set')  # Prefetch related sends for boulders
    )

def get_boulders_bar_chart_data(user_id, spraywall_id):
    # Initialize boulders_bar_chart_data
    boulders_bar_chart_data = copy.deepcopy(boulders_bar_chart_data_template)
    # Query grade counts
    grade_counts = (
        Boulder.objects
        .filter(send__person=user_id, spraywall_id=spraywall_id)
        .values('grade')
        .annotate(count=Count('grade'))
        .order_by('grade')
    )
    # Update boulders_bar_chart_data based on grade counts
    for item in grade_counts:
        for boulder_chart in boulders_bar_chart_data:
            if boulder_chart['x'] == item['grade']:
                boulder_chart['y'] = item['count']
                break
    return boulders_bar_chart_data

def get_section_boulders(section, user_id, spraywall_id):
    # section_conditions is a dictionary that maps section values to the corresponding filter conditions.
    section_conditions = {
        'likes': 'like__person',
        'bookmarks': 'bookmark__person',
        'creations': 'setter_person',
    }
    # section_condition retrieves the filter condition based on the section value.
    section_condition = section_conditions.get(section)
    # **{f"{section_condition}": user_id, "spraywall_id": spraywall_id} constructs a dictionary with the section_condition as the key (e.g., 'like__person') 
    # and user_id as the value. It also includes a fixed key-value pair for 'spraywall_id'.
    # When you pass this dictionary as an argument to Boulder.objects.filter(**{...}), the double asterisks ** unpack the dictionary, 
    # effectively turning it into keyword arguments for the filter method. So, it becomes Boulder.objects.filter(like__person=user_id, spraywall_id=spraywall_id) 
    # or the equivalent filter condition based on the selected section.
    boulders = Boulder.objects.filter(**{f"{section_condition}": user_id, "spraywall_id": spraywall_id})
    DATA = []
    for boulder in boulders:
        DATA.append(get_boulder_data(boulder, user_id))
    return DATA

def get_logbook_quick_data(boulders):
    # Calculate the total count of user's successful climbs
    return boulders.count()

def get_creations_quick_data(boulders):
    return boulders.count()

def get_likes_quick_data(user_id, spraywall_id):
    # We use filter to filter likes based on the user's person and the spraywall associated with the boulders.
    # We use aggregate to count the number of likes that match the filter criteria. The result is stored in the id__count field of the aggregation result.
    return Like.objects.filter(person=user_id, boulder__spraywall=spraywall_id).count()

def get_bookmarks_quick_data(user_id, spraywall_id):
    return Bookmark.objects.filter(person=user_id, boulder__spraywall=spraywall_id).count()

def get_top_grade_quick_data(boulders):
    # Find the top grade (hardest climbed grade difficulty)
    top_grade_obj = boulders.aggregate(Max('grade'))
    return top_grade_obj['grade__max'] if top_grade_obj['grade__max'] else '4a/V0'

def get_flashes_quick_data(boulders):
    # Total count of flashes
    flashes = 0
    sent_boulders = boulders.distinct()
    for boulder in sent_boulders:
        send_row = Send.objects.filter(boulder=boulder.id).first() # first uploaded boulder that the user ascended (not counting repeated ascents which were not uploaded first)
        if send_row.attempts == 1:
            flashes += 1
    return flashes

def get_boulder_section_quick_data(user_id, spraywall_id):
    """
    This is a docstring that provides information about my_function.

    Args:
        parameter1: Description of the first parameter.
        parameter2: Description of the second parameter.

    Returns:
        Description of the return value.

    Raises:
        Any exceptions raised by the function.
    """
    # get copy of boulders section quick data template
    boulders_section_quick_data = copy.deepcopy(boulders_section_quick_data_template)
    # logbook
    sent_boulders = Boulder.objects.filter(send__person=user_id, spraywall=spraywall_id)
    boulders_section_quick_data['Logbook'] = get_logbook_quick_data(sent_boulders)
    # creations
    boulders = Boulder.objects.filter(spraywall=spraywall_id, setter_person=user_id)
    boulders_section_quick_data['Creations'] = get_creations_quick_data(boulders)
    # likes count
    boulders_section_quick_data['Likes'] = get_likes_quick_data(user_id, spraywall_id)
    # bookmarks count
    boulders_section_quick_data['Bookmarks'] = get_bookmarks_quick_data(user_id, spraywall_id)
    # Convert the dictionary into an array of objects - simpler format for frontend use
    boulders_section_quick_data = [{'section': key, 'data': value} for key, value in boulders_section_quick_data.items()]
    return boulders_section_quick_data

def get_stats_section_quick_data(user_id, spraywall_id):
    # get copy of stats section quick data template
    stats_section_quick_data = copy.deepcopy(stats_section_quick_data_template)
    sent_boulders = Boulder.objects.filter(send__person=user_id, spraywall=spraywall_id)
    stats_section_quick_data['Top Grade'] = get_top_grade_quick_data(sent_boulders)
    stats_section_quick_data['Flashes'] = get_flashes_quick_data(sent_boulders)
    # Convert the dictionary into an array of objects - simpler format for frontend use
    stats_section_quick_data = [{'section': key, 'data': value} for key, value in stats_section_quick_data.items()]
    return stats_section_quick_data

def get_circuits_section_quick_data(user_id, spraywall_id):
    circuits = Circuit.objects.filter(person=user_id, spraywall=spraywall_id)
    circuits_section_quick_data = []
    for circuit in circuits:
        # retrieving all boulder data in particular circuit
        boulders = circuit.boulders.all()
        boulder_data = []
        for boulder in boulders:
            boulder_data.append(get_boulder_data(boulder, user_id))
        # putting boulder data inside circuits data
        circuits_section_quick_data.append({
            'id': circuit.id,
            'name': circuit.name,
            'description': circuit.description,
            'color': circuit.color,
            'private': circuit.private,
            'boulderData': boulder_data,
        })
    return circuits_section_quick_data

def  get_profile_quick_data(user_id, spraywalls):
    profile_quick_data = []
    for spraywall in spraywalls:
        if 'id' in spraywall:
            profile_quick_data.append({
                'bouldersSectionQuickData': get_boulder_section_quick_data(user_id, spraywall['id']),
                'statsSectionQuickData': get_stats_section_quick_data(user_id, spraywall['id']),
                'circuitsSectionQuickData': get_circuits_section_quick_data(user_id, spraywall['id']),
            })
    return profile_quick_data