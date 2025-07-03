#pragma once

class UnaryOperator;
class BinaryOperator;
class SecureRelation;

class planNode
{
public:
    UnaryOperator *up = nullptr;
    BinaryOperator *bp = nullptr;

    SecureRelation *input1 = nullptr;
    SecureRelation *input2 = nullptr;

    planNode *previous1 = nullptr;
    planNode *previous2 = nullptr;

    planNode *next = nullptr;
    SecureRelation *output = nullptr;

    planNode(UnaryOperator *u_op, SecureRelation *input_rel);
    planNode(UnaryOperator *u_op, planNode *child);
    planNode(BinaryOperator *bin_op, SecureRelation *input_rel1, SecureRelation *input_rel2);
    planNode(BinaryOperator *bin_op, planNode *left_child, planNode *right_child);
    planNode(BinaryOperator *bin_op, planNode *left_child, SecureRelation *input_rel2);

    SecureRelation get_output(); // Only declared here!
};
