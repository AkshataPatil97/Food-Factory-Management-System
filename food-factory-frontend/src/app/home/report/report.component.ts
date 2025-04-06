import { Component } from '@angular/core';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import { UsersService } from '../../shared/services/users.service';
import { ProductService } from '../../shared/services/product.service';
import { OrdersService } from '../../shared/services/orders.service';
import { DeliveryboyService } from '../../shared/services/deliveryboy.service';

@Component({
  selector: 'app-report',
  templateUrl: './report.component.html',
  styleUrls: ['./report.component.scss']
})
export class ReportComponent {
  constructor(
    private userService: UsersService,
    private productService: ProductService,
    private orderService: OrdersService,
    private deliveryService: DeliveryboyService
  ) { }

  reportFilters = {
    startDate: null,
    endDate: null,
    entityType: null
  };

  entityOptions = [
    { label: 'Staff', value: 'staff' },
    { label: 'Product', value: 'product' },
    { label: 'Order', value: 'order' },
    { label: 'Delivered Order', value: 'delivered_order' },
    { label: 'Cancelled Order', value: 'cancelled_order' },
    { label: 'Invoice', value: 'invoice' },
    { label: 'Delivery Boy', value: 'delivery_boy' }
  ];

  reportColumns: any[] = [];
  reportData: any[] = [];

  generateReport() {
    const { startDate, endDate, entityType } = this.reportFilters;

    if (!entityType) {
      alert("⚠️ Please select an entity type.");
      return;
    }

    const handleResponse = (response: any, type: string) => {
      console.log(`📌 ${type} API Response:`, response);
      const data = Array.isArray(response) ? response : response.data || response.results || [];
      if (!Array.isArray(data)) {
        console.error(`❌ Expected an array but got:`, response);
        return;
      }
      this.prepareReport(data, type);
    };

    switch (entityType) {
      case 'staff': {
        this.userService.fetchAllStaff().subscribe(data => {
          console.log("✅ Fetching Staff Data...", data);
          handleResponse(data.staff, 'Staff');
        });
        break;
      }
      case 'product': {
        this.productService.fetchAllProduct().subscribe((data: any) => {
          const rawProductData = data.data;
          console.log("✅ Raw Product Data Received:", rawProductData);
      
          if (!Array.isArray(rawProductData)) {
            console.error("❌ Expected an array but got:", rawProductData);
            return;
          }
      
          const formattedData = rawProductData.map((item: any[]) => ({
            id: item[0],
            name: item[1],
            code: item[2],
            category_id: item[3],
            mfg_date: item[4],
            exp_date: item[5],
            stock: item[6],
            created_at: item[7],
            updated_at: item[8],
            is_deleted: item[9] === 1 ? "Yes" : "No"
          }));
      
          console.log("✅ Formatted Product Data:", formattedData);
          this.prepareReport(formattedData, 'Product');
        });
        break;
      }
      
      case 'order': {
        this.orderService.fetchAllOrderForAdmin().subscribe(data => {
          console.log("✅ Fetching Order Data...", data);
          handleResponse(data.data, 'Order');
        });
        break;
      }
      case 'delivered_order': {
        this.orderService.fetchAllDeliveredOrderForAdmin().subscribe(data => {
          console.log("✅ Fetching Delivered Order Data...", data);
          handleResponse(data.data, 'Delivered Order');
        });
        break;
      }
      case 'cancelled_order': {
        this.orderService.fetchAllCancelledOrderForAdmin().subscribe(data => {
          console.log("✅ Fetching Cancelled Order Data...", data);
          handleResponse(data.data, 'Cancelled Order');
        });
        break;
      }
      case 'invoice': {
        this.orderService.fetchAllInvoices().subscribe(data => {
          console.log("✅ Fetching Invoice Data...", data);
          let invoiceList = data.data.map((invoice: any) => ({
            ...invoice,
            order_data: JSON.parse(invoice.order_data),
            user_data: JSON.parse(invoice.user_data)
          }));
          handleResponse(invoiceList, 'Invoice');
        });
        break;
      }
      case 'delivery_boy': {
        this.deliveryService.fetchAllDeliveryBoy().subscribe((data: any) => {
          console.log("✅ Raw Delivery Boy Data Received:", data);
          const deliveryBoys = Array.isArray(data.staff) ? data.staff : data;
          if (!Array.isArray(deliveryBoys)) {
            console.error("❌ Expected an array but got:", deliveryBoys);
            return;
          }
          console.log("✅ Formatted Delivery Boy Data:", deliveryBoys);
          this.prepareReport(deliveryBoys, 'Delivery Boy');
        });
        break;
      }
      default:
        console.warn("⚠️ Unknown entity type selected.");
    }
  }

  prepareReport(data: any[], type: string) {
    const { startDate, endDate } = this.reportFilters;
  
    const filteredData = data.filter((item: any) => {
      // Get a valid created date
      const createdRaw = item.created || item.created_at;
      if (!createdRaw) return true;
  
      const created = new Date(createdRaw);
      const start = startDate ? new Date(startDate) : null;
      const end = endDate ? new Date(endDate) : null;
  
      return (!start || created >= start) && (!end || created <= end);
    });
  
    if (filteredData.length === 0) {
      this.reportData = [];
      console.warn("⚠️ No data available for the selected entity.");
      alert("No data found for the selected filters.");
      return;
    }
  
    // Set columns dynamically
    const keys = Object.keys(filteredData[0]);
    this.reportColumns = keys.map(k => ({
      field: k,
      header: k.replace(/_/g, ' ').toUpperCase()
    }));
  
    this.reportData = filteredData;
  
    // Generate the PDF
    this.generatePDF(type, filteredData);
  }
  
  generatePDF(title: string, data: any[]) {
    const doc = new jsPDF('l');
    
    // Ensure data is properly formatted
    const rows: (string | number)[][] = data.map(item => 
      Object.values(item).map(value => (typeof value === 'string' || typeof value === 'number') ? value : JSON.stringify(value))
    );
    
    const headers = [Object.keys(data[0])];
  
    doc.text(`${title} Report`, 14, 10);
  
    autoTable(doc, {
        head: headers,
        body: rows,
        startY: 20
    });
  
    doc.save(`${title.toLowerCase().replace(' ', '_')}_report.pdf`);
  }
  
}
