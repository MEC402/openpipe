import { Injectable } from '@angular/core';
import {Observable} from 'rxjs';
import {HttpClient, HttpHeaders} from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class ChatbotService {

  botURL = 'http://localhost:5005/webhooks/rest/webhook';

  constructor(private http: HttpClient) { }

  public sendMessageToBot(messageText, sender): Observable<ChatBotResponse[]> {
    const postBody = {
      'sender': sender,
      'message': messageText,
    } ;
    const headers = new HttpHeaders({
      'Content-Type': 'text/json',
      'Access-Control-Allow-Origin': '*',
    });
    return this.http.post<ChatBotResponse[]>(this.botURL, postBody);
  }
}

class ChatBotResponse {
  recipient_id;
  text;
}
