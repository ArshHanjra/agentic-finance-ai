import { useEffect, useState } from "react";
import axios from "axios";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
} from "recharts";

function App() {
  const [data, setData] = useState(null);

  const [transactions, setTransactions] =
    useState([]);

  const [description, setDescription] =
    useState("");

  const [amount, setAmount] =
    useState("");

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const analysisResponse =
        await axios.get(
          "http://127.0.0.1:8000/full-analysis"
        );

      setData(analysisResponse.data);

      const transactionResponse =
        await axios.get(
          "http://127.0.0.1:8000/transactions"
        );

      setTransactions(
        transactionResponse.data
      );

    } catch (error) {
      console.error(error);
    }
  };

  const addTransaction = async () => {
    try {
      await axios.post(
        "http://127.0.0.1:8000/add-transaction",
        {
          description: description,
          amount: parseFloat(amount),
        }
      );

      setDescription("");
      setAmount("");

      fetchData();

    } catch (error) {
      console.error(error);
    }
  };

  if (!data) {
    return (
      <div
        style={{
          backgroundColor: "#111827",
          color: "white",
          minHeight: "100vh",
          padding: "30px",
        }}
      >
        <h1>Loading...</h1>
      </div>
    );
  }

  const chartData =
    data.budget_plan.budget_analysis;

  const COLORS = [
    "#0088FE",
    "#00C49F",
    "#FFBB28",
    "#FF8042",
    "#A855F7",
  ];

  return (
    <div
      style={{
        padding: "30px",
        fontFamily: "Arial",
        backgroundColor: "#111827",
        minHeight: "100vh",
        color: "white",
      }}
    >
      <h1>Agentic Finance AI Dashboard</h1>

      <div
        style={{
          background: "#1F2937",
          padding: "20px",
          borderRadius: "10px",
          marginTop: "20px",
        }}
      >
        <h2>Add Transaction</h2>

        <input
          type="text"
          placeholder="Description"
          value={description}
          onChange={(e) =>
            setDescription(e.target.value)
          }
          style={{
            padding: "10px",
            marginRight: "10px",
            width: "250px",
            borderRadius: "5px",
            border: "none",
          }}
        />

        <input
          type="number"
          placeholder="Amount"
          value={amount}
          onChange={(e) =>
            setAmount(e.target.value)
          }
          style={{
            padding: "10px",
            marginRight: "10px",
            width: "120px",
            borderRadius: "5px",
            border: "none",
          }}
        />

        <button
          onClick={addTransaction}
          style={{
            padding: "10px 20px",
            cursor: "pointer",
            borderRadius: "5px",
            border: "none",
            background: "#2563EB",
            color: "white",
          }}
        >
          Add
        </button>
      </div>

      <div
        style={{
          background: "#1F2937",
          padding: "20px",
          borderRadius: "10px",
          marginTop: "20px",
        }}
      >
        <h2>AI Insights</h2>

        <p>{data.insights}</p>
      </div>

      <div
        style={{
          background: "#1F2937",
          padding: "20px",
          borderRadius: "10px",
          marginTop: "20px",
        }}
      >
        <h2>Forecast</h2>

        <h3>
          ₹{" "}
          {
            data.forecast
              .predicted_next_month_spending
          }
        </h3>
      </div>

      <div
        style={{
          background: "#1F2937",
          padding: "20px",
          borderRadius: "10px",
          marginTop: "20px",
        }}
      >
        <h2>Budget Distribution</h2>

        <PieChart width={500} height={400}>
          <Pie
            data={chartData}
            dataKey="spent"
            nameKey="category"
            cx="50%"
            cy="50%"
            outerRadius={120}
            label
          >
            {chartData.map(
              (entry, index) => (
                <Cell
                  key={index}
                  fill={
                    COLORS[
                      index % COLORS.length
                    ]
                  }
                />
              )
            )}
          </Pie>

          <Tooltip />
          <Legend />
        </PieChart>
      </div>

      <div
        style={{
          background: "#1F2937",
          padding: "20px",
          borderRadius: "10px",
          marginTop: "20px",
        }}
      >
        <h2>Transaction History</h2>

        {transactions.map(
          (item, index) => (
            <div
              key={index}
              style={{
                padding: "10px",
                borderBottom:
                  "1px solid gray",
              }}
            >
              <p>
                {item.description}
              </p>

              <p>
                ₹ {item.amount}
              </p>
            </div>
          )
        )}
      </div>
    </div>
  );
}

export default App;