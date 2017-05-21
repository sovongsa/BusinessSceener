import { BsPage } from './app.po';

describe('bs App', () => {
  let page: BsPage;

  beforeEach(() => {
    page = new BsPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
