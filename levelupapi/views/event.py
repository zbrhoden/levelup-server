@action(methods=['post', 'delete'], detail=True)
def signup(self, request, pk=None):
    """Managing gamers signing up for events"""
    # Django uses the `Authorization` header to determine
    # which user is making the request to sign up
    gamer = Gamer.objects.get(user=request.auth.user)

    try:
        # Handle the case if the client specifies a game
        # that doesn't exist
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response(
            {'message': 'Event does not exist.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # A gamer wants to sign up for an event
    if request.method == "POST":
        try:
            # Using the attendees field on the event makes it simple to add a gamer to the event
            # .add(gamer) will insert into the join table a new row the gamer_id and the event_id
            event.attendees.add(gamer)
            return Response({}, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({'message': ex.args[0]})

    # User wants to leave a previously joined event
    elif request.method == "DELETE":
        try:
            # The many to many relationship has a .remove method that removes the gamer from the attendees list
            # The method deletes the row in the join table that has the gamer_id and event_id
            event.attendees.remove(gamer)
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            return Response({'message': ex.args[0]})
