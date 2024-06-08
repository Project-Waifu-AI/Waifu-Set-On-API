self.addEventListener("notificationclick", (event) => {
  notifData = event.notification.data
  event.notification.close();

  const ws = new WebSocket(`ws://localhost:8008/api/websoket/community-chat/chatting?access_token=${notifData.token}`);

  switch (event.notification.tag) {
    case "message_reply": {
      switch (event.action) {
        case "reply": {
          ws.onopen = () => {
            console.log("accept request API call.. with ", notifData);
            msg = {
              "action": notifData.action,
              "text": event.reply,
              "group": notifData.group,
              "withMedia": notifData.withMedia
            }
            ws.send(JSON.stringify(msg));
          }

          break
        }
        case "dismiss":
          {
            console.log("Message have been dismissed!")
          }

          break;
        // Handle other actions ...
      }
    }
  }
});

