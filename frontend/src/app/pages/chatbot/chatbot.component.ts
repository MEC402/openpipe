import { Component, OnInit } from '@angular/core';
import {ChatbotService} from '../../services/chatbot.service';

@Component({
  selector: 'ngx-chatbot',
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.scss'],
})
export class ChatbotComponent implements OnInit {

  constructor(private chatbotService: ChatbotService) { }

  ngOnInit() {
    this.messages.push({
      text: 'Hello! I am here to help you with any question about the world museum. How can I help you?',
      date: new Date(),
      reply: false,
      type: 'text',
      user: {
        name: 'Bot',
        avatar: 'https://cdn.dribbble.com/users/722835/screenshots/4082720/bot_icon.gif',
      },
    });
  }

  messages: any[] = [];

  sendMessage(event: any, userName: string, avatar: string, reply: boolean) {
    const files = !event.files ? [] : event.files.map((file) => {
      return {
        url: file.src,
        type: file.type,
        icon: 'file-text-outline',
      };
    });

    this.messages.push({
      text: event.message,
      date: new Date(),
      reply: reply,
      type: files.length ? 'file' : 'text',
      files: files,
      user: {
        name: userName,
        avatar: avatar,
      },
    });
    this.chatbotService.sendMessageToBot(event.message,'bot').subscribe(res => {
      res.forEach(result => {
        this.messages.push({
          text: result.text,
          date: new Date(),
          reply: !reply,
          type: files.length ? 'file' : 'text',
          files: files,
          user: {
            name: 'Bot',
            avatar: avatar,
          },
        });
      });
    });
  }

}
