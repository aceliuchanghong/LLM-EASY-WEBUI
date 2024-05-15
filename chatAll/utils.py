def predict_stream(message, history):
    history_format = []
    for human, assistant in history:
        history_format.append([human, assistant])
    model.history = history_format
    for chunk in model.predict_stream(message):
        yield chunk
