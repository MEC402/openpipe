import { NbMenuItem } from '@nebular/theme';

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
    title: 'Meta-Data',
    icon: 'bookmark-outline',
    link: '/pages/settings',
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
    title: 'Docs',
    icon: 'question-mark-circle',
    link: '/pages/docs',
  },
];
