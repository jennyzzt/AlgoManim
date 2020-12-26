from manimlib.imports import *

class DepthFirstSearch(Scene):
    def init_graph(self, adj):
        nodes = dict()
        edges = dict()

        # create nodes
        n_id = 0
        angle = 2 * np.pi / (len(adj))
        for key in adj:
            node = Circle(
                color=WHITE,
                fill_opacity=1,
                radius=0.5 / 2
            )
            txt = TextMobject(str(key))
            txt.set_color(BLACK)
            txt.scale(0.5 * 1.5)
            grp = VGroup(node, txt)

            n_angle = angle * n_id
            grp.move_to(3*np.array([np.cos(n_angle), np.sin(n_angle), 0]))

            self.add(grp)
            nodes[key] = node
            n_id += 1

        for key in adj:
            for adj_key in adj[key]:
                if key <= adj_key:
                    e_id = (key, adj_key)
                else:
                    e_id = (adj_key, key)

                if e_id not in edges:
                    line = Line(nodes[key].get_center(), nodes[adj_key].get_center())
                    edges[e_id] = line
                    self.add(line)
                    self.bring_to_back(line)

        return nodes, edges

    def construct(self):
        adj = { 'A' : [ 'B', 'C', 'F', 'G' ],
                'B' : [ 'A', 'C', 'D', 'G' ],
                'C' : [ 'A', 'B', 'G' ],
                'D' : [ 'B', 'G' ],
                'E' : [ ],
                'F' : [ 'A', 'G' ],
                'G' : [ 'A', 'B', 'C', 'D', 'F' ] }
        nodes, edges = self.init_graph(adj)

        def dfs_helper(node_key, visited):
            visited.append(node_key)
            for adj_key in adj[node_key]:
                if adj_key not in visited:
                    adj_node = nodes[adj_key]
                    if node_key <= adj_key:
                        e_id = (node_key, adj_key)
                    else:
                        e_id = (adj_key, node_key)
                    edge = edges[e_id]
                    self.play(ApplyMethod(adj_node.set_fill, RED), ApplyMethod(edge.set_color, RED))
                    dfs_helper(adj_key, visited)
                    self.play(ApplyMethod(adj_node.set_fill, WHITE), ApplyMethod(edge.set_color, WHITE))

        start_key = 'A'
        self.play(ApplyMethod(nodes[start_key].set_fill, RED))
        dfs_helper(start_key, [])