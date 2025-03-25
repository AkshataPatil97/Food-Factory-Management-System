import { Component } from '@angular/core';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.scss']
})
export class FooterComponent {
  isFooterHidden: boolean = true;

  toggleFooter() {
    this.isFooterHidden = !this.isFooterHidden;
  }

}
