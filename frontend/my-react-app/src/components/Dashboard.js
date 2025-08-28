import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, PieChart, Pie, Cell } from 'recharts';

const Dashboard = () => {
  const [orders, setOrders] = useState([]);
  const [analytics, setAnalytics] = useState({});
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
  const fetchData = async () => {
    try {
      const res = await axios.get('http://127.0.0.1:5000/orders');
      setOrders(res.data);

      const analRes = await axios.get('http://127.0.0.1:5000/analytics');
      setAnalytics(analRes.data);
    } catch (err) {
      console.error("Fetch error:", err);
    }
  };

  fetchData();

  const interval = setInterval(async () => {
    try {
      // Only call update_status once
      const updateRes = await axios.post('http://127.0.0.1:5000/update_status');
      setNotifications(updateRes.data.notifications);

      // Then refresh orders + analytics
      fetchData();
    } catch (err) {
      console.error("Update error:", err);
    }
  }, 5000);

  return () => clearInterval(interval);
}, []);


  // Prepare chart data
  const statusData = [
    { name: 'Pending', value: orders.filter(o => o.Status === 'Pending').length },
    { name: 'In-Progress', value: orders.filter(o => o.Status === 'In-Progress').length },
    { name: 'Delivered', value: orders.filter(o => o.Status === 'Delivered').length },
  ];

  return (
    <div>
      <h1>Pharma Order Tracking Dashboard</h1>
      {/* Order List Table */}
      <table>
        <thead><tr><th>OrderID</th><th>Retailer</th><th>Status</th><th>Prediction</th></tr></thead>
        <tbody>{orders.map(o => <tr key={o.OrderID}><td>{o.OrderID}</td><td>{o.RetailerName}</td><td>{o.Status}</td><td>{o.Prediction}</td></tr>)}</tbody>
      </table>

      {/* Analytics */}
      <div>
        <p>Delivered Today: {analytics.delivered_today}</p>
        <p>Delivered Yesterday: {analytics.delivered_yesterday}</p>
        <p>Delayed: {analytics.delayed}</p>
        <p>Avg Delivery Time: {analytics.avg_delivery_time}</p>
      </div>

      {/* Charts */}
      <PieChart width={400} height={300}>
        <Pie data={statusData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={100} fill="#8884d8" label>
          {statusData.map((entry, index) => <Cell key={`cell-${index}`} fill={['#ff7300', '#387908', '#00C49F'][index % 3]} />)}
        </Pie>
        <Tooltip />
      </PieChart>

      <BarChart width={600} height={300} data={orders}>
        <XAxis dataKey="AssignedDeliveryBoy" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="Distance" fill="#8884d8" />
      </BarChart>

      {/* Notification Log */}
      <div>
        <h3>Notifications</h3>
        <ul>{notifications.map((n, i) => <li key={i}>{n}</li>)}</ul>
      </div>

      {/* Simulated Progress Bar (for one order example) */}
      <progress value={orders.filter(o => o.Status === 'Delivered').length / orders.length * 100} max="100"></progress>
    </div>
  );
};

export default Dashboard;