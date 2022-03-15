import { NbMenuItem } from '@nebular/theme';
import {AssetComponent} from "./asset/asset.component";

export const MENU_ITEMS: NbMenuItem[] = [
  {
    title: 'Search',
    icon: 'search-outline',
    link: '/pages/home',
  },
  {
    title: 'Folders',
    icon: 'keypad-outline',
    link: '/pages/collections',
  },
  {
    title: 'Assets',
    icon: 'color-palette-outline',
    link: '/pages/assets',
    home: true,
  },
  {
    title: 'Topics',
    icon: 'code-outline',
    link: '/pages/topics',
  },
  {
    title: 'Faculty Templates',
    icon: 'edit-2',
    link: '/pages/layoutEditor',
  },
  {
    title: 'Uploader',
    icon: 'upload-outline',
    link: '/pages/uploader',
  },
  {
    title: 'Reports',
    icon: 'clipboard-outline',
    link: '/pages/reports',
  },
  {
    title: 'settings',
    icon: 'settings-2-outline',
    link: '/pages/settings',
  },
  {
    title: 'ChatBot',
    icon: 'message-circle-outline',
    link: '/pages/chatbot',
  },
  {
    title: 'Docs',
    icon: 'question-mark-circle',
    link: '/pages/docs',
  },
  {
    title: 'Experimental',
    icon: 'bulb-outline',
    link: '/pages/fireassets',
  },
];
