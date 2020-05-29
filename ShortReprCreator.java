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

//Essentially does the same thing as the Rankers but only gets the top 10 scoring docs
public class ShortReprCreator {
   
    public static void doPagingSearch(IndexSearcher searcher, Query query, PrintWriter writer) throws IOException {

        //Get the top 10 docs (pages) for the given query and write them to a file
        TopDocs results = searcher.search(query, 10);
        ScoreDoc[] hits = results.scoreDocs;
			
        for (int i=0; i < hits.length; i++) {
            Document doc = searcher.doc(hits[i].doc);
            String path = doc.get("path");
            writer.print(doc.get("title").replace(".txt", "") + " ");
            System.out.println((i+1) + ". " + path);
        }
    }
	
    //Repeat doPagingSearch for each page
    public static void main(String[] args) throws Exception { 
        String query_string=null;    
        String path = System.getProperty("user.dir");
        String index = path + "\\IndexOfFullRepr"; //input
        String shortTitleRepr = path + "\\ShortTitleRepr";  //ouput
        new File(shortTitleRepr).mkdir();
	    
        IndexReader reader = DirectoryReader.open(FSDirectory.open(Paths.get(index)));
        IndexSearcher searcher = new IndexSearcher(reader);
        Analyzer analyzer = new StandardAnalyzer();    
        QueryParser parser = new QueryParser("contents", analyzer);
	    
      
        Date start = new Date();
        //For each doc, use its contents as a query and call doPagingSearch
        for(int i = 0; i < reader.numDocs();i++) {
            Document doc = reader.document(i);
            String titleID = doc.get("title");
            if(titleID.equals(".DS_Store")|| titleID.equals(".txt"))
                continue;
            System.out.println(titleID);
            String contents = doc.get("contents").toString();
            query_string = contents;
            if(query_string.equals("")) continue;
            BooleanQuery.setMaxClauseCount( Integer.MAX_VALUE );
            Query query = parser.parse(QueryParser.escape(query_string));   
            System.out.println("Searching for: " + query.toString("contents"));
            PrintWriter writer = new PrintWriter(shortTitleRepr + "/" +titleID, "UTF-8");
            doPagingSearch(searcher,query, writer);
            writer.close();
            System.out.println();
        }
	    
        Date end = new Date();
        System.out.println("FINISHED IN " + (end.getTime() - start.getTime()) + " total milliseconds");
	      reader.close();
   }
    
}