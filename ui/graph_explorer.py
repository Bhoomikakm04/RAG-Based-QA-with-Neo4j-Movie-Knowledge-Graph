import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
from ui.theme import page_header, section_title


def _build_graph(rows):
    net = Network(height="650px", width="100%", bgcolor="#080c15", font_color="#e5edf9", directed=True, cdn_resources="in_line")
    net.set_options(r'''
    {
      "nodes": {"font": {"size": 16, "face": "Inter"}, "borderWidth": 2, "shadow": {"enabled": true, "color": "rgba(0,0,0,.45)", "size": 12, "x": 3, "y": 3}},
      "edges": {"arrows": {"to": {"enabled": true, "scaleFactor": 0.65}}, "font": {"size": 11, "face": "Inter", "color": "#b8c4d8", "strokeWidth": 0}, "smooth": {"type": "curvedCW", "roundness": 0.15}, "color": {"color": "#53627a", "highlight": "#8b5cf6"}},
      "physics": {"enabled": true, "barnesHut": {"gravitationalConstant": -5200, "centralGravity": 0.22, "springLength": 185, "springConstant": 0.035, "damping": 0.12}, "stabilization": {"iterations": 220}},
      "interaction": {"hover": true, "navigationButtons": true, "keyboard": true, "zoomView": true, "dragView": true, "tooltipDelay": 80}
    }
    ''')
    people, movies, years = set(), set(), {}
    for row in rows:
        people.add(row["person"]); movies.add(row["movie"]); years[row["movie"]] = row.get("released")
    for person in people:
        net.add_node(f"person::{person}", label=person, title=f"<b>Person</b><br>{person}", shape="dot", size=30, color={"background":"#5b8cff","border":"#b9ceff","highlight":{"background":"#7ea4ff","border":"#ffffff"}})
    for movie in movies:
        year = years.get(movie)
        title = f"<b>Movie</b><br>{movie}" + (f"<br>Released: {year}" if year else "")
        net.add_node(f"movie::{movie}", label=movie, title=title, shape="box", margin=12, color={"background":"#3b2f73","border":"#9b86ff","highlight":{"background":"#5845a0","border":"#ffffff"}}, font={"color":"#f7f4ff"})
    for row in rows:
        net.add_edge(f"person::{row['person']}", f"movie::{row['movie']}", label=row["relationship"], title=row["relationship"])
    return net


def render_graph_explorer(db):
    page_header("Knowledge Graph / Visualizer", "Explore the movie graph", "Search for a person and inspect the connected movie subgraph directly from Neo4j.")
    left, right = st.columns([4, 1])
    with left:
        name = st.text_input("Person name", value="Tom Cruise", placeholder="Tom Hanks", label_visibility="visible")
    with right:
        st.markdown("<div style='height:29px'></div>", unsafe_allow_html=True)
        run = st.button("Visualize graph", type="primary", use_container_width=True)

    if run:
        if not name.strip():
            st.warning("Enter a person name.")
            return
        query = """
        MATCH (p:Person)-[r:ACTED_IN|DIRECTED|PRODUCED|WROTE]->(m:Movie)
        WHERE toLower(p.name) = toLower($person)
        RETURN p.name AS person, type(r) AS relationship,
               m.title AS movie, m.released AS released
        ORDER BY released, movie LIMIT 50
        """
        try:
            rows = db.run_query(query, {"person": name.strip()})
            if not rows:
                st.info("No matching person/movie relationships were found.")
                return
            st.success(f"Live graph loaded • {len(rows)} relationships")
            net = _build_graph(rows)
            html = net.generate_html()
            wrapped = f'''<style>body{{margin:0;background:#080c15;overflow:hidden;font-family:Inter,Arial,sans-serif}} .graph-note{{position:fixed;top:10px;left:12px;z-index:10;color:#91a0b7;font-size:11px;background:rgba(8,12,21,.72);padding:6px 9px;border:1px solid rgba(148,163,184,.14);border-radius:8px}}</style><div class="graph-note">● Person &nbsp; ▪ Movie &nbsp; → Relationship</div>{html}<script>document.body.classList.add('graph-ready');</script>'''
            st.markdown('<div class="graph-shell">', unsafe_allow_html=True)
            components.html(wrapped, height=680, scrolling=False)
            st.markdown('</div>', unsafe_allow_html=True)
            with st.expander("Show retrieved graph records"):
                st.dataframe(rows, use_container_width=True)
        except Exception as e:
            st.error(f"Neo4j query failed: {e}")

    section_title("Graph schema", "The visualizer reads this schema from your live Neo4j database")
    try:
        schema = db.get_schema()
        a, b = st.columns(2)
        with a:
            st.markdown('<div class="schema-box"><div class="schema-label">Nodes</div>' + ''.join(f'<span class="schema-chip">{x}</span>' for x in schema["labels"]) + '</div>', unsafe_allow_html=True)
        with b:
            st.markdown('<div class="schema-box"><div class="schema-label">Relationships</div>' + ''.join(f'<span class="schema-chip rel">{x}</span>' for x in schema["relationships"]) + '</div>', unsafe_allow_html=True)
    except Exception as e:
        st.warning(str(e))
