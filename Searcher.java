import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.Date;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.search.BooleanQuery;

/** Simple command-line based search demo. */
public class Searcher {
   
    public static void doPagingSearch(IndexSearcher searcher, Query query, PrintWriter writer) throws IOException {

        //Get all docs that have a score > 0 (13k docs usually)
        TopDocs results = searcher.search(query, Integer.MAX_VALUE);
        ScoreDoc[] hits = results.scoreDocs;
			
        //writes all the doc names to the corresponding file, replacing the ".txt" with a space (doesn't write the score)
        for (int i=0; i < hits.length; i++) {
				    Document doc = searcher.doc(hits[i].doc);
				    String path = doc.get("path");
				    writer.print(doc.get("title").replace(".txt", "") + " ");
            //it takes a long time to print 13k lines lol. Can re-enable when doing shor title repr.
				    //System.out.println((i+1) + ". " + path + "||SCORE = " + hits[i].score);
        }  
    }
	
    /** Simple command-line based search demo. */
    public static void main(String[] args) throws Exception {  
        
        String query_string=null;
        
        //Get index directory (input) and create fullReprLists directory (output)
        String path = System.getProperty("user.dir");
        String index = path + "\\IndexOfFullRepr"; //full index path
        String fullReprLists = path + "\\fullReprLists";  //short_repr output folder
        new File(fullReprLists).mkdir();
	    
        IndexReader reader = DirectoryReader.open(FSDirectory.open(Paths.get(index)));
        IndexSearcher searcher = new IndexSearcher(reader);
        Analyzer analyzer = new StandardAnalyzer();
        QueryParser parser = new QueryParser("contents", analyzer);	    
        
        Date start = new Date();
        //For all the docs, get its contents and use them as a query and call doPagingSearch()
        for(int i = 0; i < reader.numDocs();i++) {
            Document doc = reader.document(i);
            String titleID = doc.get("title");
            if(titleID.equals(".DS_Store")|| titleID.equals(".txt"))
                continue;
            System.out.println(titleID);
            String contenuts = doc.get("contents").toString();
            query_string = contenuts;
            if(query_string.equals("")) continue;
            //set the maximum amount of clauses
            BooleanQuery.setMaxClauseCount( Integer.MAX_VALUE );
            //Parse the contents of the doc in to a query, removing unwanted chars (like ' or [])
            Query query = parser.parse(QueryParser.escape(query_string));   
            System.out.println("Searching for: " + query.toString("contents"));
            //Create a file and call doPagingSearch
            PrintWriter writer = new PrintWriter(fullReprLists + "/" +titleID, "UTF-8");
            doPagingSearch(searcher,query, writer);
            writer.close();
            System.out.println();
        }
        Date end = new Date();
        System.out.println("FINISHED IN " + (end.getTime() - start.getTime()) + " total milliseconds");
	      reader.close();
    }
}