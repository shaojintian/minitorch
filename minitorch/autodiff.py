from dataclasses import dataclass
from typing import Any, Iterable, List, Tuple

from typing_extensions import Protocol

# ## Task 1.1
# Central Difference calculation


def central_difference(f: Any, *vals: Any, arg: int = 0, epsilon: float = 1e-6) -> Any:
    r"""
    Computes an approximation to the derivative of `f` with respect to one arg.

    See :doc:`derivative` or https://en.wikipedia.org/wiki/Finite_difference for more details.

    Args:
        f : arbitrary function from n-scalar args to one value
        *vals : n-float values $x_0 \ldots x_{n-1}$
        arg : the number $i$ of the arg to compute the derivative
        epsilon : a small constant

    Returns:
        An approximation of $f'_i(x_0, \ldots, x_{n-1})$
    """
    # TODO: Implement for Task 1.1.
    #raise NotImplementedError('Need to implement for Task 1.1')
    result : float
    values_plus = list(vals)
    values_plus[arg] += epsilon
    vals_minus = list(vals)
    vals_minus[arg] -= epsilon
    f_plus = f(*values_plus)
    f_minus = f(*vals_minus) 
    return (f_plus - f_minus) / (2 * epsilon)


variable_count = 1


class Variable(Protocol):
    def accumulate_derivative(self, x: Any) -> None:
        pass

    @property
    def unique_id(self) -> int:
        pass

    def is_leaf(self) -> bool:
        pass

    def is_constant(self) -> bool:
        pass

    @property
    def parents(self) -> Iterable["Variable"]:
        pass

    def chain_rule(self, d_output: Any) -> Iterable[Tuple["Variable", Any]]:
        pass


def topological_sort(variable: Variable) -> Iterable[Variable]:
    """
    Computes the topological order of the computation graph.

    Args:
        variable: The right-most variable

    Returns:
        Non-constant Variables in topological order starting from the right.
    """
    # TODO: Implement for Task 1.4.
    #raise NotImplementedError('Need to implement for Task 1.4')
    visited = []
    topo_order = []
    
    def dfs(node: Variable):
        if node.unique_id in visited:
            return
        visited.append(node.unique_id)
        for parent in node.parents:  # 假设节点有 children 属性记录后继节点
            dfs(parent)
        topo_order.insert(0,node)
    
    dfs(variable)
    
    
    return topo_order  



def backpropagate(variable: Variable, deriv: Any) -> None:
    """
    Runs backpropagation on the computation graph in order to
    compute derivatives for the leave nodes.

    Args:
        variable: The right-most variable
        deriv  : Its derivative that we want to propagate backward to the leaves.

    No return. Should write to its results to the derivative values of each leaf through `accumulate_derivative`.
    """
    # TODO: Implement for Task 1.4.
    #raise NotImplementedError('Need to implement for Task 1.4')
    # Perform topological sort


    result = topological_sort(variable) 
    # 得到以Variable为最右节点的子节点拓扑图
    node2deriv = {}
    node2deriv[variable.unique_id] = deriv
    for n in result:
        if n.is_leaf():
            continue
        if n.unique_id in node2deriv.keys():
            deriv = node2deriv[n.unique_id]
        deriv_tmp = n.chain_rule(deriv)
        for key, item in deriv_tmp: 
            if key.is_leaf(): 
                key.accumulate_derivative(item)
                continue
            if key.unique_id in node2deriv.keys():
                # 根据 unique_id 判断是否已经计算得到部分梯度
                # !不要使用Scallar in，因为重构了__eq__
                node2deriv[key.unique_id] += item
            else:
                node2deriv[key.unique_id] = item
    





@dataclass
class Context:
    """
    Context class is used by `Function` to store information during the forward pass.
    """

    no_grad: bool = False
    saved_values: Tuple[Any, ...] = ()

    def save_for_backward(self, *values: Any) -> None:
        "Store the given `values` if they need to be used during backpropagation."
        if self.no_grad:
            return
        self.saved_values = values

    @property
    def saved_tensors(self) -> Tuple[Any, ...]:
        return self.saved_values
