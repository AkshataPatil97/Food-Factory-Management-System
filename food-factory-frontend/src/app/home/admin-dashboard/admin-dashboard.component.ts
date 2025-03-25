import { Component } from '@angular/core';
import { AuthService } from '../../shared/services/auth.service';

@Component({
  selector: 'app-admin-dashboard',
  templateUrl: './admin-dashboard.component.html',
  styleUrls: ['./admin-dashboard.component.scss']
})
export class AdminDashboardComponent {
  chartData: any;
  activeComponent: string = 'dashboard';
  selectedProductAction: string = '';
  userName: string = '';
  userId: number = 0;
  userRole: string = '';

  constructor(private authService: AuthService) {
    this.chartData = {
      labels: ['Sun', 'Mon', 'Tue', 'Wed'],
      datasets: [
        { label: 'Income', backgroundColor: '#66BB6A', data: [40, 60, 80, 100] },
        { label: 'Outcome', backgroundColor: '#EF5350', data: [50, 70, 90, 110] }
      ]
    };
  }

  ngOnInit(): void {
    this.setUserId();
  }

  logout() {
    this.authService.logout();
  }

  transactions = [
    { date: '2025-03-01', type: 'Invoice', amount: 1200, status: 'Paid' },
    { date: '2025-03-02', type: 'Subscription', amount: 250, status: 'Pending' },
    { date: '2025-03-03', type: 'Purchase', amount: 430, status: 'Paid' },
    { date: '2025-03-04', type: 'Withdrawal', amount: 800, status: 'Pending' }
  ];

  setUserId() {
    const user = this.authService.getUser();
    if (user && user.user_id) {
      this.userId = user.user_id;
      this.userRole = user.role;
      this.userName = user.user_name;
    }
  }

  setActiveComponent(component: string, productAction: string = '') {
    this.activeComponent = component;
    this.selectedProductAction = productAction;
  }

  isDashboardActive() {
    return this.activeComponent === 'dashboard';
  }
  isProfileActive() {
    return this.activeComponent === 'profile';
  }
  isSettingsActive() {
    return this.activeComponent === 'settings';
  }
  isProductActive() {
    return this.activeComponent === 'product';
  }
}
