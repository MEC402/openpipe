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
    title: 'Uploader',
    icon: 'upload-outline',
    link: '/pages/uploader',
  },
  {
    title: 'Reports',
    icon: 'clipboard-outline',
    link: '/pages/reports',
  },
];
