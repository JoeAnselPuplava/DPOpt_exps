#include "planNode.hpp"

// Dummy definitions
class SecureRelation
{
    // Add fields if needed
};

class UnaryOperator
{
public:
    SecureRelation execute(const SecureRelation &input)
    {
        return SecureRelation();
    }
};

class BinaryOperator
{
public:
    SecureRelation execute(const SecureRelation &a, const SecureRelation &b)
    {
        return SecureRelation();
    }
};

// Constructors
planNode::planNode(UnaryOperator *u_op, SecureRelation *input_rel)
    : up(u_op), input1(input_rel) {}

planNode::planNode(UnaryOperator *u_op, planNode *child)
    : up(u_op), previous1(child) {}

planNode::planNode(BinaryOperator *bin_op, SecureRelation *input_rel1, SecureRelation *input_rel2)
    : bp(bin_op), input1(input_rel1), input2(input_rel2) {}

planNode::planNode(BinaryOperator *bin_op, planNode *left_child, planNode *right_child)
    : bp(bin_op), previous1(left_child), previous2(right_child) {}

planNode::planNode(BinaryOperator *bin_op, planNode *left_child, SecureRelation *input_rel2)
    : bp(bin_op), previous1(left_child), input2(input_rel2) {}

SecureRelation planNode::get_output()
{
    SecureRelation result;
    if (up && input1)
    {
        result = up->execute(*input1);
    }
    return result;
}
