from django.contrib.messages import get_messages


def queue_messages(request):
    """
        Iterate over messages and assign to appropriate queues
    """
    # Init variables
    messages = {}
    basket_message = False
    search_message = False
    basket_messages = []
    search_messages = []
    other_messages = []

    # Create queued message class to assign additional properties to messages
    class Qmessage:
        def __init__(self, message, level, message_from, id):
            self.message = message
            self.level = level
            self.message_from = message_from
            self.id = id

        def __str__(self):
            return self.message

    # Get messages from request and iterate
    storage = get_messages(request)
    for message in storage:
        # We ensure extra_tags are comma delimited when created in views, so
        # split them to an array
        extra_tags = message.extra_tags.split(',')

        # Iterate over the tags looking for a tag that begins with 'from__'
        for tag in extra_tags:
            if tag.startswith('from__'):
                # Remove 'from__' to return the value
                message_from = tag.replace('from__', '')

                # If message_from contains '_basket' we have a basket message
                if '_basket' in message_from:
                    # Create a new Qmessage instance with required values
                    # from the current message, including creating a unique id
                    basket_message = Qmessage(
                        message.message,
                        message.level,
                        message_from,
                        message_from + '_' + str(len(basket_messages))
                    )
                    # Iterate over the tags again and look for a tag beginning
                    # with 'id__'.  If found, return the int value and assign
                    # to a new product_id attribute of the basket_message
                    for tag in extra_tags:
                        if tag.startswith('id__'):
                            basket_message.product_id = int(
                                tag.replace('id__', '')
                            )
                            break
                    break

                # if message_from is 'search' we have a search message
                elif message_from == 'search':
                    # Create a new Qmessage instance with required values from
                    # the current message, including creating a unique id
                    search_message = Qmessage(
                        message.message,
                        message.level,
                        message_from,
                        message_from + '_' + str(len(search_messages))
                    )
                    break

        # If we found a basket or search message, add the object to the
        # appropriate list
        if basket_message:
            basket_messages.append(basket_message)
        elif search_message:
            search_messages.append(search_message)
        else:
            # If we did not identify the message, then create a Qmessage
            # instance with required values from the current message, including
            # creating a unique id, and assign it to the other_messages list
            other_message = Qmessage(
                message.message,
                message.level,
                'Other'
                'Other_' + str(len(other_messages))
            )
            other_messages.append(other_message)

        # Clear the message objects prior to processing the next message
        basket_message = None
        search_message = None
        other_message = None

    # After iterating over all messages, assign lists as properties of the
    # local messages object
    if basket_messages:
        messages['basket_messages'] = basket_messages

    if search_messages:
        messages['search_messages'] = search_messages

    if other_messages:
        messages['other_messages'] = other_messages

    # Add the local messages object to context, and return it.  This ensures
    # that any check for {{ messages }} in the template will return the value
    # of messages in the context rather than the message storage
    context = {
        'messages': messages
    }

    return context
