import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../api/axios';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const PriceTrendChart = ({ productName }) => {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchHistory = async () => {
            if (!productName) return;
            try {
                const res = await api.get(`/advanced/price-history/?product=${encodeURIComponent(productName)}`);
                setHistory(res.data);
            } catch (err) {
                console.error("Failed to fetch price history", err);
            } finally {
                setLoading(false);
            }
        };
        fetchHistory();
    }, [productName]);

    if (!productName) return null;
    if (loading) return <div className="text-sm text-gray-500 animate-pulse h-48 bg-gray-100 rounded flex items-center justify-center">Loading trend data...</div>;
    
    if (history.length === 0) {
        return <div className="text-sm text-gray-500 h-48 bg-gray-50 border border-gray-100 rounded flex items-center justify-center">Not enough data for trend graph.</div>;
    }

    const data = {
        labels: history.map(item => new Date(item.timestamp).toLocaleDateString()),
        datasets: [
            {
                label: 'Price ($)',
                data: history.map(item => item.price),
                borderColor: 'rgb(59, 130, 246)',
                backgroundColor: 'rgba(59, 130, 246, 0.5)',
                tension: 0.2, // smooth lines
                pointRadius: 4,
                pointHoverRadius: 6,
            },
        ],
    };

    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
                display: false,
            },
            title: {
                display: true,
                text: 'Price History',
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return `$${context.parsed.y.toFixed(2)}`;
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: false,
                ticks: {
                    callback: function(value) {
                        return '$' + value;
                    }
                }
            }
        }
    };

    return (
        <div className="w-full bg-white p-4 rounded-xl shadow-sm border border-gray-100">
            <Line options={options} data={data} height={100} />
        </div>
    );
};

export default PriceTrendChart;
