import React,{useEffect,useState} from 'react'
import {BrowserRouter,useNavigate} from 'react-router-dom'
import {Bar} from 'react-chartjs-2'
import {Chart as ChartJS,CategoryScale,LinearScale,BarElement,Tooltip,Legend} from 'chart.js'
import api from './api'
ChartJS.register(CategoryScale,LinearScale,BarElement,Tooltip,Legend)

function Login({onLogin}) {
 const [email,setEmail]=useState('customer@example.com'),[password,setPassword]=useState('Customer@123'),[error,setError]=useState('')
 const submit=async e=>{e.preventDefault();try{const r=await api.post('/auth/login/',{email,password});localStorage.setItem('access',r.data.tokens.access);localStorage.setItem('user',JSON.stringify(r.data.user));onLogin(r.data.user)}catch{setError('Invalid email or password')}}
 return <div className="login-page"><div className="card login-card p-4"><h2 className="fw-bold mb-1">Savings<span>Pro</span></h2><p className="text-muted">Secure savings management</p><form onSubmit={submit}><input className="form-control mb-3" value={email} onChange={e=>setEmail(e.target.value)} placeholder="Email"/><input className="form-control mb-3" type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="Password"/>{error&&<div className="alert alert-danger">{error}</div>}<button className="btn btn-primary w-100">Sign in</button></form><small className="text-muted mt-3">Demo: customer@example.com / Customer@123</small></div></div>
}

function Dashboard({user}) {
 const [data,setData]=useState(null)
 useEffect(()=>{api.get('/dashboard/').then(r=>setData(r.data))},[])
 if(!data)return <div className="p-5">Loading dashboard...</div>
 const chart={labels:['Savings','Deposits','Withdrawals'],datasets:[{label:'Amount',data:[+data.total_savings,+data.total_deposits,+data.total_withdrawals]}]}
 return <div className="container-fluid p-4"><div className="d-flex justify-content-between align-items-center mb-4"><div><h3>Welcome, {user.name}</h3><p className="text-muted mb-0">{user.role} dashboard</p></div></div>
 <div className="row g-3"><Stat title="Total Savings" value={`৳ ${data.total_savings}`}/><Stat title="Total Deposits" value={`৳ ${data.total_deposits}`}/><Stat title="Withdrawals" value={`৳ ${data.total_withdrawals}`}/><Stat title="Customers" value={data.total_customers}/></div>
 <div className="row mt-4"><div className="col-lg-7"><div className="card p-3"><h5>Financial Overview</h5><Bar data={chart}/></div></div><div className="col-lg-5"><div className="card p-3"><h5>Recent Transactions</h5>{data.recent_transactions.map(x=><div className="transaction" key={x.id}><span>{x.transaction_type}<small>{new Date(x.created_at).toLocaleString()}</small></span><b>৳ {x.amount}</b></div>)}</div></div></div></div>
}
const Stat=({title,value})=><div className="col-md-6 col-xl-3"><div className="card stat p-3"><small className="text-muted">{title}</small><h4 className="mt-2 mb-0">{value}</h4></div></div>

function App(){
 const [user,setUser]=useState(()=>JSON.parse(localStorage.getItem('user')||'null'))
 if(!user)return <Login onLogin={setUser}/>
 return <div><nav className="navbar navbar-expand-lg bg-white border-bottom px-4"><b className="navbar-brand">Savings<span>Pro</span></b><div className="ms-auto d-flex gap-3 align-items-center"><span>{user.name}</span><button className="btn btn-outline-danger btn-sm" onClick={()=>{localStorage.clear();setUser(null)}}>Logout</button></div></nav><Dashboard user={user}/></div>
}
export default function Root(){return <BrowserRouter><App/></BrowserRouter>}
