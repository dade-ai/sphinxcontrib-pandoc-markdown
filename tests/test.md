
```math
\newcommand{\V}[1]{\mathbf{#1}}
\begin{aligned}
\V{y} &= \tanh(W_{k,f} * \V{x} + V^T_{k,f} * \V{h}) \odot  σ(W_{k,g} * \V{x} + V^T_{k,g} * \V{h}) \\

\V{y} &= \tanh(W_{k,f} * \V{x} + V_{k,f} * \V{s}) \odot  σ(W_{k,g} * \V{x} + V_{k,g} * \V{s})
\end{aligned}
```

