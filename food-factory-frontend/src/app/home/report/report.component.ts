import { Component } from '@angular/core';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import { UsersService } from '../../shared/services/users.service';
import { ProductService } from '../../shared/services/product.service';
import { OrdersService } from '../../shared/services/orders.service';
import { DeliveryboyService } from '../../shared/services/deliveryboy.service';
import { MessageService } from 'primeng/api';

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
    private messageService: MessageService,
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
  reportPreviewed: boolean = false;

  onEntityChange(event: any) {
    this.generateReport();
  }

  filterByDateRange(data: any[], startDate: string | null, endDate: string | null): any[] {
    // If no dates are provided, return the data as is
    if (!startDate || !endDate) return data;

    const start = new Date(startDate);
    const end = new Date(endDate);

    return data.filter((item: any) => {
      const createdAt = new Date(item.created_at || item.order_date || item.issuedAt || item.invoice.issued_at || item.created_at);
      return createdAt >= start && createdAt <= end;
    });
  }

  generateReport() {
    const { startDate, endDate, entityType } = this.reportFilters;

    this.reportData = [];
    this.reportColumns = [];
    this.reportPreviewed = false;

    // Check for missing entity type
    if (!entityType) {
      this.showMessage('warn', 'Warn', '⚠️ Please select an entity type.!')
      return;
    }

    // Handle API response and format the data
    const handleResponse = (response: any, type: string) => {
      console.log(`📌 ${type} API Response:`, response);
      const data = Array.isArray(response) ? response : response.data || response.results || [];
      if (!Array.isArray(data)) {
        console.error(`❌ Expected an array but got:`, response);
        return;
      }
      this.prepareReport(data, type);
    };

    // Fetch and process data based on the selected entity type
    switch (entityType) {
      case 'staff': {
        this.userService.fetchAllStaff().subscribe((data: any) => {
          const rawStaffData = data.staff;
          console.log("✅ Raw Staff Data Received:", rawStaffData);

          if (!Array.isArray(rawStaffData)) {
            console.error("❌ Expected an array but got:", rawStaffData);
            return;
          }

          // Filter the data based on the provided date range
          const filteredData = this.filterByDateRange(rawStaffData, startDate, endDate);

          // Format the data
          const formattedData = filteredData.map((item: any) => ({
            id: item.id,
            name: item.name,
            phone: item.phone,
            alternate_phone: item.alternate_phone,
            address: item.address,
            staff_type: item.staff_type,
            order_id: item.order_id ?? 'N/A',
            created_at: item.created_at,
            updated_at: item.updated_at,
            is_deleted: item.is_deleted === 1 ? "Yes" : "No",
            is_available: item.is_available === 1 ? "Yes" : "No"
          }));

          console.log("✅ Formatted Staff Data:", formattedData);
          this.prepareReport(formattedData, 'Staff');
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
      
          const filteredData = this.filterByDateRange(rawProductData, startDate, endDate);
      
          const formattedData = filteredData.map((item: any) => ({
            id: item.id,
            name: item.product_name,
            code: item.product_code,
            category_id: item.category_id,
            mfg_date: item.manufacturing_date,
            exp_date: item.expiry_date,
            price: item.price,
            created_at: item.created_at,
            updated_at: item.updated_at,
            is_deleted: item.is_deleted === 1 ? "Yes" : "No"
          }));
      
          console.log("✅ Formatted Product Data:", formattedData);
          this.prepareReport(formattedData, 'Product');
        });
        break;
      }      

      case 'order': {
        this.orderService.fetchAllOrderForAdmin().subscribe((data: any) => {
          const rawOrderData = data.data;
          console.log("✅ Raw Order Data Received:", rawOrderData);

          if (!Array.isArray(rawOrderData)) {
            console.error("❌ Expected an array but got:", rawOrderData);
            return;
          }

          const filteredData = this.filterByDateRange(rawOrderData, startDate, endDate);

          const formattedOrderData = filteredData.map((item: any) => ({
            orderId: item.order_id,
            userName: item.user.username,
            userShopName: item.user.shop_name,
            userMobileNo: item.user.mobile_no,
            orderTotalPrice: item.total_price,
            orderStatus: item.status,
            orderDate: item.order_date,
            orderItems: item.order_items.map((orderItem: any) =>
              `Product: ${orderItem.product_name}, Qty: ${orderItem.quantity}, Price: ${orderItem.price_at_order}`
            ).join('; ')
          }));

          console.log("✅ Formatted Order Data:", formattedOrderData);
          this.prepareReport(formattedOrderData, 'Order');
        });
        break;
      }

      case 'delivered_order': {
        this.orderService.fetchAllDeliveredOrderForAdmin().subscribe((data: any) => {
          const rawDeliveredData = data.data;
          console.log("✅ Raw Delivered Data Received:", rawDeliveredData);

          if (!Array.isArray(rawDeliveredData)) {
            console.error("❌ Expected an array but got:", rawDeliveredData);
            return;
          }

          const filteredData = this.filterByDateRange(rawDeliveredData, startDate, endDate);

          const formattedDeliveredData = filteredData.map((item: any) => ({
            orderId: item.order_id,
            userName: item.user.username,
            userShopName: item.user.shop_name,
            userMobileNo: item.user.mobile_no,
            orderTotalPrice: item.total_price,
            orderStatus: item.status,
            orderDate: item.order_date,
            orderItems: item.order_items.map((orderItem: any) =>
              `Product: ${orderItem.product_name}, Qty: ${orderItem.quantity}, Price: ${orderItem.price_at_order}`
            ).join('; ')
          }));

          console.log("✅ Formatted Delivered Order Data:", formattedDeliveredData);
          this.prepareReport(formattedDeliveredData, 'Delivered Order');
        });
        break;
      }

      case 'cancelled_order': {
        this.orderService.fetchAllCancelledOrderForAdmin().subscribe((data: any) => {
          const rawCancelledData = data.data;
          console.log("✅ Raw Cancelled Data Received:", rawCancelledData);

          if (!Array.isArray(rawCancelledData)) {
            console.error("❌ Expected an array but got:", rawCancelledData);
            return;
          }

          const filteredData = this.filterByDateRange(rawCancelledData, startDate, endDate);

          const formattedCancelledData = filteredData.map((item: any) => ({
            orderId: item.order_id,
            userName: item.user.username,
            userShopName: item.user.shop_name,
            userMobileNo: item.user.mobile_no,
            orderTotalPrice: item.total_price,
            orderStatus: item.status,
            orderDate: item.order_date,
            orderItems: item.order_items.map((orderItem: any) =>
              `Product: ${orderItem.product_name}, Qty: ${orderItem.quantity}, Price: ${orderItem.price_at_order}`
            ).join('; ')
          }));

          console.log("✅ Formatted Cancelled Order Data:", formattedCancelledData);
          this.prepareReport(formattedCancelledData, 'Cancelled Order');
        });
        break;
      }

      case 'invoice': {
        this.orderService.fetchAllInvoices().subscribe((data: any) => {
          console.log("✅ Fetching Invoice Data...", data);

          // Parse and transform invoice data
          let invoiceList = data.data.map((invoice: any) => {
            const orderData = JSON.parse(invoice.order_data);
            const userData = JSON.parse(invoice.user_data);

            return {
              orderId: orderData.order_id,
              orderDate: orderData.order_date,
              totalPrice: orderData.total_price,
              orderStatus: orderData.status,
              isCancelled: orderData.is_cancelled ? 'Yes' : 'No',
              cancellationReason: orderData.cancellation_reason,
              username: userData.username,
              shopName: userData.shop_name,
              email: userData.email,
              mobileNo: userData.mobile_no,
              address: this.getFormattedAddress(JSON.parse(userData.address_payload)),
              totalAmount: invoice.total_amount,
              invoiceStatus: invoice.status,
              issuedAt: invoice.issued_at,
            };
          });

          console.log("✅ Original Invoice Data:", invoiceList);

          // Filter by date range (if provided)
          const filteredInvoices = this.filterByDateRange(invoiceList, startDate, endDate);

          console.log("✅ Filtered Invoice Data:", filteredInvoices);

          // Prepare the report with the filtered data
          this.prepareReport(filteredInvoices, 'Invoice');
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

          const filteredData = this.filterByDateRange(deliveryBoys, startDate, endDate);

          const formattedData = filteredData.map((item: any) => ({
            id: item.id,
            name: item.name,
            phone: item.phone,
            alternate_phone: item.alternate_phone,
            address: item.address,
            delivery_area: item.delivery_area,
            created_at: item.created_at,
            updated_at: item.updated_at,
            is_deleted: item.is_deleted === 1 ? "Yes" : "No",
            is_available: item.is_available === 1 ? "Yes" : "No"
          }));

          console.log("✅ Formatted Delivery Boy Data:", formattedData);
          this.prepareReport(formattedData, 'Delivery Boy');
        });
        break;
      }

      default:
        this.showMessage('warn', 'Warn', '⚠️ Invalid entity type selected!')
        break;
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
      this.showMessage('warn', 'Warn', '⚠️ No data found for the selected filters.!')
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

    // Define the headers based on the keys of the first item in the data
    const headers = [Object.keys(data[0])];

    doc.text(`${title} Report`, 14, 10);

    // Check if column length exceeds 6 or 7 columns
    const maxColumnsPerPage = 10; // You can adjust this value based on your requirement
    const splitHeaders = [];
    const splitRows = [];

    // Split columns and rows if necessary
    if (headers[0].length > maxColumnsPerPage) {
      const firstHalfHeaders = headers[0].slice(0, maxColumnsPerPage);
      const secondHalfHeaders = headers[0].slice(maxColumnsPerPage);

      splitHeaders.push(firstHalfHeaders, secondHalfHeaders);

      const firstHalfRows = rows.map(row => row.slice(0, maxColumnsPerPage));
      const secondHalfRows = rows.map(row => row.slice(maxColumnsPerPage));

      splitRows.push(firstHalfRows, secondHalfRows);
    } else {
      splitHeaders.push(headers[0]);
      splitRows.push(rows);
    }

    // Render tables for the first set of columns
    autoTable(doc, {
      head: [splitHeaders[0]],
      body: splitRows[0],
      startY: 20,
      theme: 'grid',
      margin: { top: 15 },
      didDrawPage: (data) => {
        if (splitHeaders.length > 1) {
          // Check if we need to add a page for the remaining columns
          if (data.cursor && data.cursor.y > doc.internal.pageSize.height - 40) {
            doc.addPage();
            doc.text(`${title} Report`, 14, 10);
          }
        }
      },
      headStyles: {
        fillColor: [255, 255, 0],  // Yellow background for header
        textColor: [0, 0, 0],       // Dark black text for header
      },
      styles: {
        textColor: [0, 0, 0],       // Dark black text for all cells
      }
    });

    // Render tables for the second set of columns (on a new page)
    if (splitHeaders.length > 1) {
      doc.addPage();
      autoTable(doc, {
        head: [splitHeaders[1]],
        body: splitRows[1],
        startY: 20,
        theme: 'grid',
        margin: { top: 15 },
        didDrawPage: (data) => {
          if (data.cursor && data.cursor.y > doc.internal.pageSize.height - 40) {
            doc.addPage();
          }
        },
        headStyles: {
          fillColor: [255, 255, 0],  // Yellow background for header
          textColor: [0, 0, 0],       // Dark black text for header
        },
        styles: {
          textColor: [0, 0, 0],       // Dark black text for all cells
        }
      });
    }

    this.showMessage('success', 'Success', `✅ ${title} report generated successfully!`);
    // Save the PDF
    doc.save(`${title.toLowerCase().replace(' ', '_')}_report.pdf`);
  }

  getFormattedAddress(address: any): string {
    if (address && Object.keys(address).length > 0) {
      const { street, landmark, city, state, zip } = address;
      return `${street}, ${landmark}, ${city}, ${state} - ${zip}`;
    }
    return 'Address not available';
  }

  showMessage(strSeverity: string, strSummary: string, strDetail: string) {
    this.messageService.add({ severity: strSeverity, summary: strSummary, detail: strDetail });
  }

}
