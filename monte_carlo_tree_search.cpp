#include <cstdint>
#include <iostream>
#include <vector>
#include <map>
#include <string>

const int8_t DEALER_PLAYER = -1;

class Node
{
public:
  Node * parent;
  int8_t acting_player;
  int16_t CFR;
  uint32_t visits;
  std::map<std::string, Node *> children;
  
  Node(Node * parent, int8_t acting_player)
  {
    Node::parent        = parent;
    Node::acting_player = acting_player;
    Node::CFR           = 0;
    Node::visits        = 0;
  }
  
  void create_child(Node * p_parent_node, int8_t acting_player, std::string key);
  Node * get_child(Node * p_node, std::string key);
  int8_t get_acting_player(Node * p_node);
  int16_t get_CFR(Node * p_node);
  uint32_t get_visits(Node * p_node);
};

Node * create_root_node()
{
  Node root_node = new Node(NULL, DEALER_PLAYER);
  return &root_node;
}

void Node::create_child(Node * p_parent_node, int8_t acting_player, std::string key)
{
  Node child_node = new Node(p_parent_node, acting_player);
  p_parent_node->children[key] = &child_node;
}

Node * Node::get_child(Node * p_node, std::string key)
{
  return p_node->children[key];
}

int8_t Node::get_acting_player(Node * p_node)
{
  return p_node->acting_player;
}

int16_t Node::get_CFR(Node * p_node)
{
  return p_node->CFR;
}

uint32_t Node::get_visits(Node * p_node)
{
  return p_node->visits;
}

/*
void strategy_user_input(std::vector<Node> player_nodes, Holdem holdem)
{
}
*/
