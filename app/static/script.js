function toggleRefresh() {
    if(refresh) {
        refresh = false;
        $("#toggle").text("Unpause");
        toast("Updates Paused", "The graph will not be updated automatically.");
    } else {
        refresh = true;
        $("#toggle").text("Pause");
        toast("Updates Resumed", "Every 8 seconds we will check to see if the previous graph has finished drawing. If so, we will pull a new one for you automatically.");
    }
    $("#refresh").toggle();
    $("#saveMe").toggle();
}

function saveGraph(mode, view, variable) {
    $.ajax({
        url: "/generate?mode=" + mode + "&view=SAVE",
        type: "GET",
        success: function(data) {
            var output = "";
            if(view == "LIVE")
                output = JSON.parse(data)["filenames"][0];
            else
                output = variable.split("/")[3];
            var formData = "filename=" + output;
            $.ajax({
                url: "/save",
                type: "POST",
                data: formData,
                success: function(data) {
                    toast("Graph Saved", "Graph has been saved successfully to " + data);
                },
                error: function(data) {
                    toast("Save Error", "Failed to export graph data. Could not save.");
                }
            });
        },
        error: function(data) {
            toast("Save Error", "Failed to retrieve graph data. Could not save.");
        }
    });
}

function hidePopover() {
    $('#ip_link').focus();
}

function hideTooltips() {
    $('[rel="tooltip"]').tooltip("hide"); // hide all tooltips
    $('.url_lookup').blur(); // remove focus from link when clicked
}

function toast(title, content) {
    $("#toast-header").html(title);
    $("#toast-body").html(content);
    $(".toast").toast('show');
}

function exportData(data, node, mode) {
    $(".export").blur(); // remove focus from link when clicked
    var formData = "data=" + data + "&mode=" + mode + "&node=" + node;
    $.ajax({
        url : "/export",
        type: "POST",
        data : formData,
        success: function(data, textStatus, jqXHR)
        {
            toast("Data Exported", "Data exported to: app/static/exports/" + data);
        },
        error: function (jqXHR, textStatus, errorThrown)
        {
            toast("Export Failed", "Data failed to export");
        }
    });
}

function drawGraph(userInit, view, variable, mode) {
    pendingDraw = true;
    hideTooltips();
    hidePopover();
    $.ajax({
        url: "/generate?mode=" + mode + "&view=" + view,
        type: 'GET',
        success: function(res) {
            var filenames = JSON.parse(res);
            var current = "";
            if(view == "LIVE")
                current = "/static/PrevSnapshots/" + filenames["filenames"][0];
            else
                current = variable;  
            $("#save_links").html(function() {
                var output = "";

                filenames["filenames"].forEach(function(e, i) {
                    if(current.indexOf(e) != -1)
                        output += "<b><a href='/snapshot/" + e + "'>" + e + "</a></b><br>";
                    else
                        output += "<a href='/snapshot/" + e + "'>" + e + "</a><br>";
                })
                return output;
            });

            d3.select('svg').selectAll('*').remove();
            d3.json(current, function(error, graph) {
                if (error) throw error;

                var elementSelector = '.graph',
                        svgSelector = '#svg-graph',
                        width = 960,
                        height = 600, isDragging;

                var lScale = d3.scale.pow().exponent(5)
                            .range([3, 15])
                            .domain(d3.extent(graph.links, function(d) {
                                return d.value; }));
                                
                var zoomBeh = d3.behavior.zoom()
                            .scaleExtent([0.1, 10])
                            .on("zoom", zoomEvent);
                var svgParent = d3.select(svgSelector)
                            .attr("width", width)
                            .attr("height", height);
                var svg = svgParent
                            .call(zoomBeh)
                            .append("g");

                var edges = [];
                graph.links.forEach(function(e) { 
                    var sourceNode = graph.nodes.filter(function(n) { return n.id === e.source; })[0],
                    targetNode = graph.nodes.filter(function(n) { return n.id === e.target; })[0];
                    edges.push({source: sourceNode, target: targetNode, value: e.value, weight: e.weight});
                });

                var force = d3.layout.force()
                            .charge(-60)
                            .linkDistance(function(d) { return lScale(d.value); })
                            .size([width, height])
                            .nodes(graph.nodes)
                            .links(edges)
                            .on('start', forceStart)
                            .start();

                var link = svg.selectAll(".link")
                            .data(edges)
                            .enter().append("line")
                            .attr("class", function(d,i) {
                                if(d.value == 1)
                                    return "tcp" + " weight_" + Math.min(5, d.weight);
                                return "udp" + " weight_" + Math.min(5, d.weight);
                            });

                var drag = force.drag()
                            .on("dragstart", function(d){
                                isDragging = true;
                                d3.event.sourceEvent.stopPropagation();
                            })
                            .on("dragend", function(d) {
                                isDragging = false;
                            });

                var node = svg.selectAll(".node")
                            .data(graph.nodes)
                            .enter().append("circle")
                            .attr("class", function(d,i) { 
                                if(d.group == 1)
                                    return "node source";
                                return "node dest";
                            })
                            .attr("r", function(d){ return 3;})
                            .style("fill", function(d) {
                                if(d.group == 0)
                                    return "#AEC7E8"; // source node
                                else if(d.group == 1)
                                    return "#1F77B4"; // destination node
                                return "#A8A6A6"; // hybrid node
                            })
                            .attr("tabindex", function(d) {
                                return 0;
                            })
                            .attr("role", function(d) {
                                return "button";
                            })
                            .attr("data-toggle", function(d) {
                                return "popover";
                            })
                            .attr("data-trigger", function(d) {
                                return "focus";
                            })
                            .attr("data-html", function(d) {
                                return "true";
                            })
                            .attr("title", function(d) {
                                var data = d.id + "," + d.group + "," + d.weight + "\\n";
                                for(var i = 0; i < d.srcIPs.length; i++) {
                                    data += d.srcIPs[i] + ":" + d.srcPORT[i] + " --> " + d.dstIPs[i] + ":" + d.dstPORT[i] + "\\n";
                                }
                                var output = "Details for <b>";
                                if(mode == "IP" && d.URL != "Unknown")
                                    output += "<a class='url_lookup' href='javascript:hideTooltips();' rel='tooltip' title='" + d.URL + "'>";
                                output += d.id;
                                if(mode == "IP" && d.URL != "Unknown")
                                    output += "</a>";
                                output += "</b> &nbsp;&nbsp;&nbsp;<a class='export' href='#' onmousedown='javascript:exportData(\"" + data + "\", \"" + d.id + "\", \"" + mode + "\")'>Export</a>";

                                return output;
                            })
                            .attr("data-content", function(d) {
                                var output = "";
                                for(var i = 0; i < d.srcIPs.length; i++) {
                                    var src_match = true, dst_match = true;

                                    if(d.srcIPs[i] != d.id) {
                                        output += d.srcIPs[i];
                                        src_match = false;
                                    }

                                    if(d.srcPORT[i] != d.id) {
                                        if(!src_match)
                                            output += ":";
                                        output += d.srcPORT[i];
                                    }

                                    output += " → ";

                                    if(d.dstIPs[i] != d.id) {
                                        if(d.URLs[i] != "Unknown")
                                            output += "<a href='javascript:hideTooltips();' rel='tooltip' title='" + d.URLs[i] + "'>" + d.dstIPs[i] + "</a>";
                                        else
                                            output += d.dstIPs[i];
                                        dst_match = false;
                                    }

                                    if(d.dstPORT[i] != d.id) {
                                        if(!dst_match)
                                            output += ":";
                                        output += d.dstPORT[i];
                                    }
                                    output += "<br>";
                                }
                                return output;
                            })
                            .call(drag);

                node.append("title")
                    .text(function(d) { 
                        if(mode == "IP")
                            return "IP: " + d.id;
                        return "PORT: " + d.id;
                    });

                function forceStart() {
                    var ticksPerRender = 3;
                    requestAnimationFrame(function render() {
                    for (var i=0; i<ticksPerRender; i++)
                      force.tick();
                    link.attr("x1", function(d) { return d.source.x; })
                      .attr("y1", function(d) { return d.source.y; })
                      .attr("x2", function(d) { return d.target.x; })
                      .attr("y2", function(d) { return d.target.y; });
                    node.attr("cx", function(d) { return d.x; })
                      .attr("cy", function(d) { return d.y; });
                    if (force.alpha() > 0) {
                      requestAnimationFrame(render);
                    }
                    zoomFit(undefined, 0);
                  });
                }

                function zoomEvent() {
                    hidePopover();
                    node
                    .attr("r", function(d) { return 5 / d3.event.scale; })
                    .style("stroke-width", function(d) {
                        return 2 / d3.event.scale;});
                  link.style('stroke-width', 1 / d3.event.scale);
                  svg.attr("transform",
                            "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
                }

                function zoomFit(paddingPercent, transitionDuration) {
                    var bounds = svg.node().getBBox();
                    var parent = svg.node().parentElement;
                    var fullWidth = parent.clientWidth || parent.parentNode.clientWidth,
                        fullHeight = parent.clientHeight || parent.parentNode.clientHeight;
                    var zwidth = bounds.width,
                        zheight = bounds.height;
                    var midX = bounds.x + zwidth / 2,
                        midY = bounds.y + zheight / 2;
                    if (zwidth == 0 || zheight == 0) return; // nothing to fit
                    var scale = (paddingPercent || 0.95) / Math.max(zwidth / fullWidth, zheight / fullHeight);
                    var translate = [fullWidth / 2 - scale * midX, fullHeight / 2 - scale * midY];

                    //console.trace("zoomFit", translate, scale);
                    svg
                        .transition()
                        .duration(transitionDuration || 0) // milliseconds
                        .call(zoomBeh.translate(translate).scale(scale).event);
                }

                $('[data-toggle="popover"]').popover({
                    sanitize: false
                });

                $('[rel="tooltip"]').tooltip();
                
                $('circle').mousedown(function(e) {
                    e.stopImmediatePropagation();
                    e.preventDefault(); // prevent focus from firing
                });
                $('circle').click(function(e) {
                    $(this).focus();
                    $('[rel="tooltip"]').tooltip();
                });

                if(userInit)
                    toast("Graph Refreshed", "New data loaded to graph");
                pendingDraw = false;
            });
        },
        error: function(data) {
            toast("Refresh Failed", "Failed to refresh graph contents");
        }
    });
}

function getExport(file) {
    $.ajax({
        url: "/getExport?file=" + file,
        type: 'GET',
        success: function(res) {
            $("#contents").html(function() {
                return res;
            });
            toast("Export Loaded", "Contents of export file loaded successfully.");
        },
        error: function(res) {
            toast("Export Retrieval Error", "Unable to retrieve contents of the selected export file.");
        }
    });
}