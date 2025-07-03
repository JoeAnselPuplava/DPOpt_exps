#include <iostream>
#include <fstream>
#include <memory>
#include <string>
#include <nlohmann/json.hpp>
#include <cstdlib>
#include "planNode.hpp" // Your existing planNode class declaration

using json = nlohmann::json;

// Dummy classes for SecureRelation, UnaryOperator, and BinaryOperator
class SecureRelation
{
};
class UnaryOperator
{
public:
    SecureRelation execute(const SecureRelation &input) { return SecureRelation(); }
};
class BinaryOperator
{
public:
    SecureRelation execute(const SecureRelation &a, const SecureRelation &b) { return SecureRelation(); }
};

// Dummy factory functions for operators
UnaryOperator *createUnaryOp(const std::string &name)
{
    std::cout << "Creating UnaryOperator: " << name << std::endl;
    return new UnaryOperator();
}
BinaryOperator *createBinaryOp(const std::string &name)
{
    std::cout << "Creating BinaryOperator: " << name << std::endl;
    return new BinaryOperator();
}
SecureRelation *createRelation(const std::string &name)
{
    std::cout << "Creating SecureRelation: " << name << std::endl;
    return new SecureRelation();
}

// Recursively builds the planNode from JSON
planNode *build_plan(const json &node)
{
    if (node.is_object())
    {
        for (auto &[key, val] : node.items())
        {
            if (key.find("select") != std::string::npos)
            {
                // Unary operator
                planNode *child = build_plan(val);
                UnaryOperator *uop = createUnaryOp(key);
                return new planNode(uop, child);
            }
            else if (key.find("join") != std::string::npos)
            {
                // Binary operator
                auto it = val.items();
                auto left = build_plan(val[it.begin().key()]);
                auto right = build_plan(val[std::next(it.begin()).key()]);
                BinaryOperator *bop = createBinaryOp(key);
                return new planNode(bop, left, right);
            }
            else if (key.find("r") != std::string::npos)
            {
                return new planNode(nullptr, createRelation(key));
            }
        }
    }
    return nullptr;
}

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        std::cerr << "Usage: ./planner <Query>\n";
        return 1;
    }

    std::string query = argv[1];
    // std::cout << query;

    std::string command = "python3 get_cost.py \"" + query + "\"";
    int status = system(command.c_str());

    if (status == 0)
    {
        std::ifstream file("test.json");
        if (!file)
        {
            std::cerr << "Failed to open file\n";
            return 1;
        }

        json j;
        file >> j;

        planNode *root = build_plan(j["root"]);
        std::cout << "Execution complete.\n";
    }
    else
    {
        std::cout << "Error running python script";
    }
    return 0;

    // Optional: call root->get_output(); or free memory

    return 0;
}
